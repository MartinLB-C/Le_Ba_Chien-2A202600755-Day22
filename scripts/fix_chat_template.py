import json

file_path = r"d:\VIn_GD2\day22\Le_Ba_Chien-2A202600755-Day22\colab\Lab22_DPO_T4.ipynb"

with open(file_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source_text = "".join(cell["source"])
        
        # Look for the tokenizer pad_token patch, which is in the cells loading the base model
        if "tokenizer.pad_token = tokenizer.eos_token" in source_text and "from unsloth.chat_templates import get_chat_template" not in source_text:
            new_source = []
            for line in cell["source"]:
                new_source.append(line)
                if "tokenizer.pad_token = tokenizer.eos_token" in line:
                    indent = line.split("tokenizer.pad_token")[0]
                    # We add get_chat_template right after it
                    new_source.append(f'{indent}from unsloth.chat_templates import get_chat_template\n')
                    new_source.append(f'{indent}tokenizer = get_chat_template(tokenizer, chat_template="chatml")\n')
            cell["source"] = new_source

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
