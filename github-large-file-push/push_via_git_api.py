#!/usr/bin/env python3
"""Push a local file to GitHub via Git Data API (blob→tree→commit→ref).
Works for large files that exceed the Contents API 1MB limit.
Uses OAuth token from WorkBuddy connector tokens directory.

Usage:
    python push_via_git_api.py <local_file_path> <repo_path_in_github> <commit_message>
    python push_via_git_api.py /path/to/audio_l04.js audio_l04.js "Update audio data"

Environment variables (optional):
    GITHUB_OWNER - repo owner (default: auto-detect from git remote)
    GITHUB_REPO  - repo name (default: auto-detect from git remote)
    GITHUB_TOKEN - override token path (default: auto-find in connectors/)
"""
import requests
import base64
import json
import os
import sys
import subprocess
from pathlib import Path

def find_github_token():
    """Find GitHub OAuth token from WorkBuddy connector tokens."""
    tokens_dir = Path.home() / '.workbuddy' / 'connectors'
    if not tokens_dir.exists():
        print(f"ERROR: Connectors directory not found: {tokens_dir}", file=sys.stderr)
        sys.exit(1)
    for connector_dir in tokens_dir.iterdir():
        token_file = connector_dir / 'tokens' / 'github.txt'
        if token_file.exists():
            return token_file.read_text().strip()
    print("ERROR: No GitHub token found in connectors/", file=sys.stderr)
    sys.exit(1)

def get_git_remote_info(repo_dir):
    """Get owner and repo from git remote URL."""
    r = subprocess.run(
        ['git', '-C', repo_dir, 'remote', 'get-url', 'origin'],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print("ERROR: Failed to get git remote URL", file=sys.stderr)
        sys.exit(1)
    url = r.stdout.strip()
    # Parse: https://github.com/owner/repo.git or git@github.com:owner/repo.git
    if 'github.com/' in url:
        parts = url.split('github.com/')[1].replace('.git', '').split('/')
    elif 'github.com:' in url:
        parts = url.split('github.com:')[1].replace('.git', '').split('/')
    else:
        print(f"ERROR: Unsupported remote URL: {url}", file=sys.stderr)
        sys.exit(1)
    return parts[0], parts[1]

def main():
    if len(sys.argv) < 3:
        print("Usage: python push_via_git_api.py <local_file> <github_path> [commit_message]", file=sys.stderr)
        sys.exit(1)

    local_file = os.path.abspath(sys.argv[1])
    github_path = sys.argv[2]
    commit_msg = sys.argv[3] if len(sys.argv) > 3 else f"Update {github_path}"

    if not os.path.exists(local_file):
        print(f"ERROR: Local file not found: {local_file}", file=sys.stderr)
        sys.exit(1)

    # Get credentials
    token = os.environ.get('GITHUB_TOKEN') or find_github_token()
    owner = os.environ.get('GITHUB_OWNER')
    repo = os.environ.get('GITHUB_REPO')

    if not owner or not repo:
        repo_dir = os.path.dirname(local_file)
        # Walk up to find .git
        while not os.path.exists(os.path.join(repo_dir, '.git')):
            parent = os.path.dirname(repo_dir)
            if parent == repo_dir:
                print("ERROR: Cannot find git repo root", file=sys.stderr)
                sys.exit(1)
            repo_dir = parent
        owner, repo = get_git_remote_info(repo_dir)
        print(f"Detected: {owner}/{repo}")

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json'
    }
    api = f'https://api.github.com/repos/{owner}/{repo}'

    # 1. Read file and create blob
    with open(local_file, 'rb') as f:
        content_b64 = base64.b64encode(f.read()).decode('ascii')
    print(f"Creating blob ({len(content_b64)} chars)...")
    r = requests.post(f'{api}/git/blobs', headers=headers,
                      json={'content': content_b64, 'encoding': 'base64'})
    if r.status_code != 201:
        print(f"ERROR: Blob creation failed: {r.status_code} {r.text[:200]}", file=sys.stderr)
        sys.exit(1)
    blob_sha = r.json()['sha']
    print(f"Blob: {blob_sha}")

    # 2. Get latest commit and tree
    r = requests.get(f'{api}/git/ref/heads/main', headers=headers)
    if r.status_code != 200:
        print(f"ERROR: Get ref failed: {r.status_code}", file=sys.stderr)
        sys.exit(1)
    commit_sha = r.json()['object']['sha']
    print(f"Latest commit: {commit_sha}")

    r = requests.get(f'{api}/git/commits/{commit_sha}', headers=headers)
    base_tree_sha = r.json()['tree']['sha']
    print(f"Base tree: {base_tree_sha}")

    # 3. Create new tree
    r = requests.post(f'{api}/git/trees', headers=headers, json={
        'base_tree': base_tree_sha,
        'tree': [{
            'path': github_path,
            'mode': '100644',
            'type': 'blob',
            'sha': blob_sha
        }]
    })
    if r.status_code != 201:
        print(f"ERROR: Tree creation failed: {r.status_code} {r.text[:200]}", file=sys.stderr)
        sys.exit(1)
    new_tree_sha = r.json()['sha']
    print(f"New tree: {new_tree_sha}")

    # 4. Create commit
    r = requests.post(f'{api}/git/commits', headers=headers, json={
        'message': commit_msg,
        'tree': new_tree_sha,
        'parents': [commit_sha]
    })
    if r.status_code != 201:
        print(f"ERROR: Commit creation failed: {r.status_code} {r.text[:200]}", file=sys.stderr)
        sys.exit(1)
    new_commit_sha = r.json()['sha']
    print(f"New commit: {new_commit_sha}")

    # 5. Update branch ref
    r = requests.patch(f'{api}/git/refs/heads/main', headers=headers, json={
        'sha': new_commit_sha,
        'force': False
    })
    if r.status_code != 200:
        print(f"ERROR: Branch update failed: {r.status_code} {r.text[:200]}", file=sys.stderr)
        sys.exit(1)
    print(f"Branch updated!")
    print(f"https://github.com/{owner}/{repo}/commit/{new_commit_sha}")

if __name__ == '__main__':
    main()
