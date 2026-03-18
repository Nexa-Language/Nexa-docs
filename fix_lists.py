import os
import re

import glob

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find a line that is NOT a list item, NOT empty, 
    # followed immediately by a line that IS a list item (- ...)
    
    # We replace:
    # \n(something not starting with - or empty)
    # \n- ...
    
    # Let's just use re.sub
    # Lookbehind for a non-newline, non-space character
    # We want: 
    # (.*?[^\n\s].*?)\n(\s*-\s.*) -> add \n between them
    
    lines = content.split('\n')
    new_lines = []
    
    in_code_block = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            
        if not in_code_block and re.match(r'^\s*-\s', line):
            # Check previous line
            if i > 0 and lines[i-1].strip() != '' and not re.match(r'^\s*-\s', lines[i-1]):
                new_lines.append('')
        
        new_lines.append(line)
        
    new_content = '\n'.join(new_lines)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

for fp in glob.glob("docs/**/*.md", recursive=True):
    fix_file(fp)

