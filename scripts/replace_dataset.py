import json

def replace_in_ipynb(filepath, old_text, new_text):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    for cell in nb.get('cells', []):
        if 'source' in cell:
            for i, line in enumerate(cell['source']):
                if old_text in line:
                    cell['source'][i] = line.replace(old_text, new_text)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

def replace_in_py(filepath, old_text, new_text):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(old_text, new_text)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

replace_in_ipynb('colab/Lab22_DPO_T4.ipynb', '5CD-AI/Vietnamese-alpaca-cleaned', 'bkai-foundation-models/vi-alpaca')
replace_in_ipynb('colab/Lab22_DPO_BigGPU.ipynb', '5CD-AI/Vietnamese-alpaca-cleaned', 'bkai-foundation-models/vi-alpaca')
replace_in_py('notebooks/01_sft_mini.py', '5CD-AI/Vietnamese-alpaca-cleaned', 'bkai-foundation-models/vi-alpaca')
replace_in_py('README.md', '5CD-AI/Vietnamese-alpaca-cleaned', 'bkai-foundation-models/vi-alpaca')
