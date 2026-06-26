import json

path = r'D:\VIn_GD2\day22\Le_Ba_Chien-2A202600755-Day22\colab\Lab22_DPO_T4.ipynb'
out_path = r'D:\VIn_GD2\day22\Le_Ba_Chien-2A202600755-Day22\colab\Lab22_DPO_T4_Part1to4.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cut_index = -1
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        source = "".join(cell.get('source', []))
        if '# ⏵ Stage from `notebooks/05_merge_deploy_gguf.py`' in source:
            cut_index = i
            break

if cut_index != -1:
    nb['cells'] = nb['cells'][:cut_index]
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"Successfully removed part 5 and 6. Saved cut notebook to {out_path}")
else:
    print("Could not find part 5 to cut")
