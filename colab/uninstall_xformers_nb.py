import json

path = r'D:\VIn_GD2\day22\Le_Ba_Chien-2A202600755-Day22\colab\Lab22_DPO_T4_Part1to4.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell.get('source', [])
        if any("Cài đặt unsloth và các thư viện khác trước" in line for line in source):
            # If not already added
            if not any("pip uninstall xformers -y" in line for line in source):
                source.append("\n# Xóa xformers để tránh lỗi backward pass trên GPU T4 (Kaggle)\n")
                source.append("!pip uninstall xformers -y\n")
            break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Added xformers uninstall to notebook")
