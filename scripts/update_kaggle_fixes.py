import json
import os

file_path = r"d:\VIn_GD2\day22\Le_Ba_Chien-2A202600755-Day22\colab\Lab22_DPO_T4.ipynb"

with open(file_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        
        # Sửa lỗi 1: Biên dịch llama-cpp-python cho GPU
        if '!pip install "llama-cpp-python"' in source or '!pip install -q "llama-cpp-python"' in source:
            new_source = []
            for line in cell["source"]:
                if "llama-cpp-python" in line and "pip install" in line:
                    new_source.append('!CMAKE_ARGS="-DGGML_CUDA=on" pip install -q "llama-cpp-python>=0.3,<1.0" --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121\n')
                else:
                    new_source.append(line)
            cell["source"] = new_source

        # Sửa lỗi 2: Quản lý API Key bảo mật trên Kaggle
        if 'os.environ.get("OPENAI_API_KEY")' in source and "judge_with_openai" in source:
            secrets_code = """import os
try:
    from kaggle_secrets import UserSecretsClient
    user_secrets = UserSecretsClient()
    
    # Lấy key từ hệ thống Secrets của Kaggle
    try:
        os.environ["OPENAI_API_KEY"] = user_secrets.get_secret("OPENAI_API_KEY")
        print("Đã load OPENAI_API_KEY từ Kaggle Secrets.")
    except:
        pass
        
    try:
        os.environ["ANTHROPIC_API_KEY"] = user_secrets.get_secret("ANTHROPIC_API_KEY")
        print("Đã load ANTHROPIC_API_KEY từ Kaggle Secrets.")
    except:
        pass
except ImportError:
    print("Không chạy trên Kaggle hoặc thư viện kaggle_secrets không tồn tại.")

"""
            # Insert this code at the beginning of the cell
            if "kaggle_secrets" not in source:
                cell["source"] = [secrets_code] + cell["source"]

        # Sửa lỗi 3: Xử lý lỗi đa luồng (OOM / Freeze) của lm-eval
        if "def run_lm_eval" in source:
            new_source = []
            for line in cell["source"]:
                if "def run_lm_eval" in line:
                    new_source.append('import os\nos.environ["OMP_NUM_THREADS"] = "4"\n\n')
                    new_source.append(line)
                elif '"--device"' in line:
                    new_source.append('        "--device", "cuda:0",\n')
                else:
                    new_source.append(line)
            cell["source"] = new_source

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Đã áp dụng các sửa đổi thành công!")
