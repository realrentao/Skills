#!/usr/bin/env python3
"""Regenerate ALL audio files from the CURRENT generate_exams.py data"""
import os, json, base64, asyncio, glob

# === CONFIG: adjust these for your environment ===
REPO_DIR = r"<repo-dir>"  # replace with actual path
VOICE = "it-IT-IsabellaNeural"

def get_all_scripts():
    """Extract all listening scripts from the current generator data"""
    gen_py = os.path.join(REPO_DIR, "generate_exams.py")
    with open(gen_py, "r", encoding="utf-8") as f:
        content = f.read()
    
    scripts = {}
    local_vars = {}
    exec(content, local_vars)
    EXAMS = local_vars.get("EXAMS", {})
    
    for exam_key, exam_data in EXAMS.items():
        etype = exam_data["exam_type"]
        level = exam_data["level"]
        set_name = exam_data.get("set", etype)
        
        for section in exam_data.get("sections", []):
            if section["id"] == "ascolto":
                for idx, item in enumerate(section["items"]):
                    script_text = item.get("script", "")
                    if script_text:
                        key = f"{etype}_{set_name}_{level}_{idx}"
                        scripts[key] = {
                            "exam_type": etype,
                            "set": set_name,
                            "level": level,
                            "idx": idx,
                            "script": script_text
                        }
    return scripts

async def gen_mp3(text, path):
    proc = await asyncio.create_subprocess_exec(
        "edge-tts", "--voice", VOICE, "--rate", "+5%", "--text", text,
        "--write-media", path,
        stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
    await proc.communicate()
    return os.path.exists(path) and os.path.getsize(path) > 1000

async def main():
    scripts = get_all_scripts()
    print(f"Total listening scripts: {len(scripts)}")
    
    done = 0
    for key, info in sorted(scripts.items()):
        etype = info["exam_type"]
        set_name = info["set"]
        level = info["level"]
        idx = info["idx"]
        script_text = info["script"]
        
        # Determine filename: CELI uses level_map (different naming), CILS uses simple level suffix
        if etype == "CELI":
            level_map = {"A1":"impatto_a1","A2":"1_a2","B1":"2_b1","B2":"3_b2","C1":"4_c1","C2":"5_c2_celi"}
            lv_part = level_map.get(level, level.lower())
            fname = f"ascolto_{idx+1}_{lv_part}"
        else:
            fname = f"ascolto_{idx+1}_{level.lower()}"
        
        audio_dir = os.path.join(REPO_DIR, etype, set_name, level, "audio")
        os.makedirs(audio_dir, exist_ok=True)
        
        mp3_path = os.path.join(audio_dir, fname + ".mp3")
        js_path = os.path.join(audio_dir, fname + ".js")
        
        print(f"  {set_name}/{level}: {fname}", end=" ", flush=True)
        
        ok = await gen_mp3(script_text, mp3_path)
        if not ok:
            print("FAIL")
            continue
        
        # Convert MP3 to base64 JS with callback pattern
        with open(mp3_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        escaped = json.dumps("data:audio/mpeg;base64," + b64)
        js_content = "(function(){var b64=" + escaped + ";if(window._audioLoaded)window._audioLoaded(b64);})();"
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(js_content)
        
        # Clean up MP3 to save space (optional - comment out if you want to keep MP3s)
        # os.remove(mp3_path)
        
        sz = os.path.getsize(js_path) // 1024
        print(f"OK {sz}KB")
        done += 1
    
    print(f"\n✅ {done}/{len(scripts)} audio files regenerated")

if __name__ == "__main__":
    asyncio.run(main())
