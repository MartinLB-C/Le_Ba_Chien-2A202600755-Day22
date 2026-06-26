import os
import glob

# Also patch all the individual python scripts in notebooks/ directory
scripts = glob.glob(r"d:\VIn_GD2\day22\Le_Ba_Chien-2A202600755-Day22\notebooks\*.py")

for file_path in scripts:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if "tokenizer.pad_token = tokenizer.eos_token" in line:
            indent = line.split("tokenizer.pad_token")[0]
            new_lines.append(f'{indent}from unsloth.chat_templates import get_chat_template\n')
            new_lines.append(f'{indent}tokenizer = get_chat_template(tokenizer, chat_template="chatml")\n')
            
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
