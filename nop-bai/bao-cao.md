# Báo cáo Day 21 — CI/CD cho AI Systems

**Nguyễn Ngọc Bảo · MSSV 2A202602951 · K4 · 07/10/2026**  
[Repository công khai](https://github.com/KeepGoing132/K4-L3L4-Track2-Day21-Nguyen_Ngoc_Bao-2A202602951-CI-CD-for-AI-Systems) · AWS S3 + EC2, `ap-southeast-2`.

## 1. Chọn siêu tham số

| Thí nghiệm MLflow | Số cây | Learning rate | Depth | F1 | Accuracy |
|---|---:|---:|---:|---:|---:|
| 1 | 100 | 0.10 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 150 | 0.10 | 4 | 0.7156 | 0.8760 |
| 4 | 200 | 0.10 | 5 | 0.7149 | 0.8740 |

Chọn **150 cây, learning rate 0.1, max depth 4** vì F1 cao nhất trong bốn
thí nghiệm bước 1 trên batch1, vượt ngưỡng 0.65. Accuracy của thí nghiệm 1 cao hơn nhưng F1
thấp hơn. Chưa đủ bằng chứng để kết luận mô hình không overfitting.

## 2. Vì sao dùng F1

Adult có khoảng 24.8% mẫu thu nhập >50K. Luôn đoán thu nhập thấp vẫn đạt
accuracy khoảng 75.2%, trong khi F1 lớp dương bằng 0. Vì vậy Quality Gate dùng
F1 của lớp >50K, kết hợp precision và recall của lớp cần đánh giá. Macro F1
trung bình đều hai lớp; weighted F1 lấy trọng số theo số mẫu, nên không tương
đương F1 lớp dương dùng trong lab.

## 3. Khó khăn và cách xử lý

Test từng ghi đè model thật: chuyển sang thư mục tạm và MLflow store riêng.
Chỉ upload model tại Release sau Quality Gate; API trả 503 nếu thiếu model và
Release kiểm tra cả health/dự đoán. Ghép batch có kiểm tra phần cuối file để
chạy lại không nhân đôi dữ liệu. Tài khoản giới hạn region nên dùng Sydney;
xác minh fingerprint ECDSA từ console output EC2 để sửa lỗi SSH. Bật lại
Actions và thêm glob `data/*.dvc` để kiểm chứng trigger từ commit dữ liệu.
**19 unit tests đã qua** trên GitHub Actions.

## 4. Kết quả CI/CD thực tế

| GitHub Actions | Mẫu train | Mẫu holdout | F1 | Accuracy |
|---|---:|---:|---:|---:|
| [Bước 2](https://github.com/KeepGoing132/K4-L3L4-Track2-Day21-Nguyen_Ngoc_Bao-2A202602951-CI-CD-for-AI-Systems/actions/runs/37607586482) | 22,361 | 500 | 0.7156 | 0.8760 |
| [Bước 3](https://github.com/KeepGoing132/K4-L3L4-Track2-Day21-Nguyen_Ngoc_Bao-2A202602951-CI-CD-for-AI-Systems/actions/runs/37607657033) | 44,722 | 500 | 0.7248 | 0.8800 |

Cả hai lần chạy có bốn job xanh. Bước 3 tự kích hoạt bởi commit **chỉ đổi
`data/train_batch1.csv.dvc`**, sau khi dữ liệu mới đã được DVC đẩy lên S3.
Trên cùng holdout, F1 tăng 0.0092 và accuracy tăng 0.0040 khi thêm dữ liệu cùng
nguồn; chưa chứng minh khả năng tổng quát hóa trên nguồn khác.

[Thử model yếu](https://github.com/KeepGoing132/K4-L3L4-Track2-Day21-Nguyen_Ngoc_Bao-2A202602951-CI-CD-for-AI-Systems/actions/runs/37606981690): F1 0.6051 làm Quality Gate
fail, Release skipped; VersionId và ETag model S3 trước/sau giống nhau.
API `http://54.253.158.211:8080` trả health OK và dự đoán hợp lệ.
Số liệu, trạng thái job và kiểm tra API lưu tại [ket-qua-cloud.json](ket-qua-cloud.json);
ảnh thật trong [anh-chup-man-hinh/](anh-chup-man-hinh/).
