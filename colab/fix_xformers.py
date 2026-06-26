import json

path = r'D:\VIn_GD2\day22\Le_Ba_Chien-2A202600755-Day22\colab\Lab22_DPO_T4_Part1to4.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell.get('source', [])
        if 'from unsloth import FastLanguageModel\n' in source:
            idx = source.index('from unsloth import FastLanguageModel\n')
            if 'UNSLOTH_USE_XFORMERS' not in "".join(source):
                source.insert(idx, "import os\n")
                source.insert(idx+1, "os.environ[\"UNSLOTH_USE_SDPA\"] = \"1\"\n")
                source.insert(idx+2, "os.environ[\"UNSLOTH_USE_XFORMERS\"] = \"0\"\n")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Fixed xformers config in notebook")
