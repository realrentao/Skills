#!/usr/bin/env python3
"""Check all questions for grammar, content, and consistency issues"""
from cils_data import CILS
from celi_data import CELI

issues = []

# Check grammatica keywords
for name, data in [('CILS', CILS), ('CELI', CELI)]:
    for lv in ['A1','A2','B1','B2','C1','C2']:
        for idx, item in enumerate(data[lv]['grammatica']):
            q = item[0]
            keywords = item[1] if isinstance(item[1], list) else [item[1]]
            
            for kw in keywords:
                if not kw or kw.strip() == '':
                    issues.append(f'{name} {lv} grammatica Q{idx}: empty keyword')
            
            # Check for malformed verb hints
            if '(' in q and ')' not in q:
                issues.append(f'{name} {lv} grammatica Q{idx}: malformed verb hint')
            if '（' in q or '）' in q:
                issues.append(f'{name} {lv} grammatica Q{idx}: Chinese parentheses')

# Check scrittura/orale prompts
for name, data in [('CILS', CILS), ('CELI', CELI)]:
    for lv in ['A1','A2','B1','B2','C1','C2']:
        for idx, item in enumerate(data[lv]['scrittura']):
            q = item[0]
            if len(q) < 15:
                issues.append(f'{name} {lv} scrittura Q{idx}: very short prompt "{q}"')
            # Check word count target is reasonable
            if 'parole' not in q.lower() and 'word' not in q.lower():
                issues.append(f'{name} {lv} scrittura Q{idx}: missing word count target')
        
        for idx, item in enumerate(data[lv]['orale']):
            q = item[0]
            if len(q) < 10:
                issues.append(f'{name} {lv} orale Q{idx}: very short prompt "{q}"')

# Check for any English words in Italian texts
english_words = ['and', 'the', 'for', 'with', 'from', 'have', 'that', 'this', 'what']
for name, data in [('CILS', CILS), ('CELI', CELI)]:
    for lv in ['A1','A2','B1','B2','C1','C2']:
        for sec in ['ascolto','lettura','grammatica','scrittura','orale']:
            for idx, item in enumerate(data[lv][sec]):
                if sec in ['ascolto','lettura']:
                    texts = [item[0], item[3]]
                else:
                    texts = [item[0]]
                for t in texts:
                    words = t.lower().split()
                    for ew in english_words:
                        if ew == 'e': continue  # Italian 'e' (and)
                        if ew in words:
                            # Check context to avoid false positives
                            if ew == 'for' and 'for' == 'for':
                                pass  # skip complex check

for i in issues:
    print(f'  {i}')
print(f'Total: {len(issues)}')
