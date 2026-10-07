# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Nguyễn Ngọc Bảo |
| MSSV | 2A202602951 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/KeepGoing132/K4-L3L4-Track2-Day21-Nguyen_Ngoc_Bao-2A202602951-CI-CD-for-AI-Systems |
| Ngày kiểm tra local | 07/10/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 150 | 0.1 | 4 | 0.7156 | 0.8760 |

**Bộ siêu tham số đã chọn:** `n_estimators=150`, `learning_rate=0.1`, `max_depth=4`.

**Lý do:** Trong ba thí nghiệm MLflow cục bộ trên, bộ tham số này có F1 cao nhất (0.7156), vượt ngưỡng 0.65. Lần 1 có accuracy cao hơn nhưng F1 thấp hơn; chưa đủ bằng chứng để kết luận mô hình không overfitting.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Adult có khoảng 24.8% mẫu thu nhập >50K. Luôn đoán lớp thu nhập thấp vẫn đạt accuracy khoảng 75.2% nhưng F1 lớp dương bằng 0. F1 lớp dương kết hợp precision và recall của đúng lớp cần đánh giá; macro F1 trung bình đều hai lớp, còn weighted F1 dùng trọng số theo số mẫu, nên hai chỉ số này không tương đương ngưỡng F1 lớp dương của lab.

---

## 3. Vấn Đề Đã Sửa và Kiểm Tra

| Vấn đề | Cách giải quyết | Kiểm tra |
|---|---|---|
| Test ghi đè model thật | Thư mục tạm và MLflow store riêng | Test huấn luyện và đường dẫn tùy chọn |
| Model không đạt vẫn ghi đè trên cloud | Chỉ Release upload sau Quality Gate | Kiểm tra workflow và các giá trị F1 biên/NaN |
| API báo khỏe dù thiếu model | HTTP 503 và kiểm tra thêm `/score` khi release | Test API; gọi API local với model thật |
| Ghép lại batch làm trùng dữ liệu | So sánh batch ở cuối file trước khi ghép | Test chạy hai lần, giữ nguyên mẫu trùng hợp lệ |

---

## 4. So Sánh Dữ Liệu Bước 2 và Bước 3 — Chạy Local

| | f1_score | accuracy |
|---|---|---|
| 22.361 mẫu, chỉ `train_batch1` | 0.7156 | 0.8760 |
| 44.722 mẫu, ghép `train_batch2` | 0.7248 | 0.8800 |

**Nhận xét:** Kiểm tra local trên cùng holdout 500 mẫu cho thấy F1 tăng khoảng 0.0092 và accuracy tăng 0.0040 khi thêm dữ liệu cùng nguồn. Kết quả chi tiết lưu tại [ket-qua-local.json](ket-qua-local.json); chúng xác nhận huấn luyện local, chưa chứng minh CI/CD tự động hoặc triển khai VM.

**Còn thiếu trước khi nộp:** remote GCS `labstore`, `dvc push`, VM/Secrets và bằng chứng ảnh 02–05 từ lần chạy cloud thực tế.
