import json

with open('colab/Lab22_DPO_T4.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell['cell_type'] == 'code':
        source = cell['source']
        for i, line in enumerate(source):
            if 'os.environ["COMPUTE_TIER"] = "T4"' in line:
                source.insert(i+1, 'os.environ["HF_DATASETS_TRUST_REMOTE_CODE"] = "1"\n')
                break
        else:
            continue
        break

with open('colab/Lab22_DPO_T4.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
