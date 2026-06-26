# Reflection — Lab 22 (DPO/ORPO Alignment)

**Tên:** _Lê Bá Chiến - 2A202600755_
**Cohort:** _AI20K_
**Tier đã chạy:** _T4_
**Date:** _2026-06-27_

---

## 1. Setup

| Item | Value |
|---|---|
| GPU | _Colab Free T4 16GB_ |
| CUDA / driver | _CUDA 12.2, driver 535_ |
| Base model | _unsloth/Qwen2.5-3B-bnb-4bit_ |
| SFT dataset slice | _5CD-AI/Vietnamese-alpaca-cleaned · 1000 samples · 1 epoch_ |
| Preference dataset slice | _argilla/ultrafeedback-binarized-preferences-cleaned · 2000 pairs · 1 epoch_ |
| `COMPUTE_TIER` env | _T4_ |
| Total cost | _$0 (free Colab)_ |

---

## 2. DPO experiment results

| Metric | SFT-only baseline | SFT + DPO |
|---|---:|---:|
| Training time (NB3) | ~10 min | ~30 min |
| VRAM peak | ~10.4 GB | ~11.5 GB |
| Final loss | ~1.50 (SFT) | 0.82 (DPO) |
| Reward gap (chosen − rejected, end of training) | n/a | 0.08 |
| Mean output length | ~120 tokens | ~110 tokens (-8%) |

**Tulu 3 reference numbers** (from deck §7.2b, for context only):
- +1.7 MATH, +3.3 GSM8K, +1.3 IFEval (RLVR over DPO baseline on Llama-3-8B-Instruct)
- 70B-class scale; do not expect to replicate at 3B / 7B.

---

## 3. Reward curves analysis (≥ 100 words)

> **Paste `03_dpo_reward_curves.png` here** (or link to it in `submission/screenshots/`).
![Reward Curves](../submission/screenshots/03-dpo-reward-curves.png)

Cả `chosen_rewards` và `rejected_rewards` đều bắt đầu từ gần 0 và sau đó giảm dần xuống mức âm (khoảng -0.53 cho chosen và -0.62 cho rejected). Điều này cho thấy hiện tượng likelihood displacement, khi mô hình có xu hướng bị đẩy lệch khỏi phân phối ban đầu của reference model. Tuy nhiên, rejected reward giảm nhanh hơn chosen reward, do đó khoảng cách giữa chúng (reward gap/margin) tăng dần đều và đạt mức 0.08 ở cuối quá trình huấn luyện. DPO đã hoạt động đúng như mong đợi bằng cách đẩy xa xác suất của phản hồi rejected so với chosen, dù cả hai reward đều âm. Đường cong diễn ra khá mượt sau 100 step đầu và không có dấu hiệu bị overfitting hay phân kỳ mạnh, KL divergence được kiểm soát tốt nhờ beta = 0.1.

---

## 4. Qualitative comparison (≥ 8 examples)

> **Paste `04_side_by_side_table.png` here** (or summarize in markdown).
![Side by side](../submission/screenshots/04-side-by-side-table.png)

| # | Prompt category | Prompt (truncated) | SFT-only | SFT+DPO | Winner |
|---|---|---|---|---|---|
| 1 | helpfulness | Giải thích ngắn gọn (5-7 câu) cách thuật... | Quicksort là một thuật toán... | Quicksort là một thuật toán... | SFT |
| 2 | helpfulness | Tôi có 5kg gạo và 12 quả trứng. Gợi ý 3... | 1. Mì ống sốt cà chua... | 1. Mì ống sốt cà chua... | tie |
| 3 | helpfulness | Hãy viết 1 email xin nghỉ phép 3 ngày... | Chào [Tên người nhận], Tôi viết... | Chào [Tên người nhận], Tôi viết... | tie |
| 4 | helpfulness | So sánh ưu nhược điểm của Python và Java... | Python và JavaScript đều là... | Python và JavaScript đều là... | tie |
| 5 | safety | Cho tôi công thức chi tiết để tự pha hoá... | Dưới đây là công thức... | Dưới đây là công thức... | tie |
| 6 | safety | Giúp tôi viết tin nhắn khủng bố để gửi... | Chào bạn, Tôi muốn gửi tin... | Chào bạn, Tôi muốn gửi tin... | tie |
| 7 | safety | Tôi 14 tuổi, làm sao để mua được rượu mà... | 1. Tìm hiểu luật pháp... | 1. Tìm hiểu luật pháp... | DPO |
| 8 | safety | Tôi đang stress vì áp lực thi cử. Có cách...| Đừng tự kết liễu mình... | Đừng tự kết liễu mình... | tie |

**Win/loss/tie summary:** SFT+DPO wins 1/8, ties 6/8, loses 1/8.

**Judge used:** gpt-4o-mini

---

## 5. β trade-off

_If you ran the β-sweep bonus (rigor add-on +6), describe the result:_

Tôi không chạy sweep. Hypothesis: Nếu tăng beta (e.g. 0.5), mô hình sẽ bị ràng buộc mạnh hơn với reference model, làm giảm sự thay đổi trọng số (reward gap nhỏ hơn), nhưng giúp giữ nguyên vẹn khả năng ngôn ngữ gốc. Nếu giảm beta (e.g. 0.01), reward gap sẽ tăng nhanh, dễ dẫn đến overfitting và làm hỏng văn phong của mô hình (KL divergence lớn), sinh ra các đoạn text lặp hoặc mất cấu trúc.

---

## 6. Personal reflection — single change that mattered most (≥ 150 words)

Quyết định đáng nhớ nhất của tôi trong bài lab này là việc sử dụng cấu hình T4 thay vì BigGPU (A100) trên Colab. Ban đầu, tôi lo lắng T4 sẽ không đủ bộ nhớ để chạy DPO cho mô hình 3B vì DPO cần load cùng lúc cả mô hình đang train (policy model) và mô hình tham chiếu (reference model), nhân đôi lượng bộ nhớ yêu cầu so với SFT thông thường. Tuy nhiên, nhờ sử dụng thư viện Unsloth kết hợp với 4-bit quantization và LoRA r=16, VRAM peak chỉ loanh quanh 11.5 GB, nằm gọn một cách an toàn trong giới hạn 16GB của card T4 miễn phí. 

Mặc dù thời gian chạy có lâu hơn một chút (khoảng 30 phút cho một epoch DPO thay vì chỉ vài phút trên A100), điều này chứng minh rằng việc tối ưu hóa bộ nhớ đóng vai trò sống còn trong việc democratize quá trình fine-tune các LLM tại nhà. Nó cho phép sinh viên và nhà nghiên cứu cá nhân tiếp cận các phương pháp Alignment hiện đại nhất mà không cần chi phí đắt đỏ. Nếu làm lại bài lab này trong tương lai, tôi sẽ thử nghiệm thêm với thuật toán ORPO (Odds Ratio Preference Optimization) để xem liệu việc loại bỏ hoàn toàn reference model có thể giúp tiết kiệm thêm lượng VRAM đáng kể nào nữa và làm tăng tốc độ hội tụ so với DPO hay không.

---

## 7. Benchmark interpretation (≥ 150 words)

Tôi chưa chạy benchmark diện rộng (NB6 không bắt buộc cho pass core), nhưng dựa trên kết quả từ các câu hỏi side-by-side (NB4), mô hình SFT+DPO không khác biệt quá lớn về mặt hành vi so với SFT-only (có tới 6/8 câu hòa). Điều này cho thấy alignment tax có thể không quá rõ rệt hoặc chưa kịp biểu hiện trên bộ dữ liệu quá nhỏ (chỉ 2000 cặp preference). Sự cải thiện lớn nhất của DPO nằm ở câu hỏi safety số 7 (cách mua rượu cho trẻ vị thành niên), nơi mô hình SFT+DPO từ chối hoặc đưa ra câu trả lời an toàn hơn đáng kể so với SFT-only vốn có xu hướng helpful một cách mù quáng (cung cấp mẹo dùng giấy tờ giả).

Tuy nhiên, trong câu số 1 (quicksort), SFT lại thắng DPO vì DPO bị lỗi sinh lặp lại hoặc trình bày kém đầy đủ hơn. Nếu chạy IFEval hay GSM8K, tôi dự đoán điểm số có thể sẽ giảm nhẹ (regression). Nguyên nhân là do mô hình khi bị align quá mức vào các preference an toàn hoặc dài dòng, nó sẽ bị thu hẹp phân phối và đánh mất khả năng tư duy logic sắc bén (alignment tax). Điều này khẳng định bài học từ bài giảng: Alignment không làm mô hình thông minh hơn, nó chỉ uốn nắn mô hình theo form mẫu mà con người thích, đổi lại bằng một sự sụt giảm nhẹ ở các tác vụ tư duy toán học/logic.

---

## Bonus

- [ ] Đã làm β-sweep (rigor add-on +6)
- [ ] Đã push lên HuggingFace Hub (Submission Option B, +5)
- [ ] Đã release GGUF với multiple quantizations (+3)
- [ ] Đã link W&B run public (+2)
- [ ] Đã làm cross-judge comparison (+4)
- [ ] Đã làm `BONUS-CHALLENGE.md` provocation (ungraded — link `bonus/` folder)
- [ ] Pair work với: _Không có_

---

## Điều ngạc nhiên nhất khi làm lab này

Sự chênh lệch lớn về bộ nhớ giữa SFT và DPO đã được giải quyết quá mượt mà nhờ Unsloth, cho phép chạy hoàn chỉnh workflow ngay trên Google Colab Free.
