# Bằng chứng nộp bài Day 21

**Nguyễn Ngọc Bảo · 2A202602951 · K4**

- [x] [Repository công khai](https://github.com/KeepGoing132/K4-L3L4-Track2-Day21-Nguyen_Ngoc_Bao-2A202602951-CI-CD-for-AI-Systems) chứa code, workflow và DVC metadata.
- [x] MLflow có ít nhất ba bộ siêu tham số và đủ F1/accuracy.
- [x] [Bước 2](https://github.com/KeepGoing132/K4-L3L4-Track2-Day21-Nguyen_Ngoc_Bao-2A202602951-CI-CD-for-AI-Systems/actions/runs/37607586482): cả bốn job thành công trên 22.361 mẫu.
- [x] [Bước 3](https://github.com/KeepGoing132/K4-L3L4-Track2-Day21-Nguyen_Ngoc_Bao-2A202602951-CI-CD-for-AI-Systems/actions/runs/37607657033): commit chỉ cập nhật dữ liệu tự kích hoạt cả bốn job, train 44.722 mẫu.
- [x] [Thử Quality Gate](https://github.com/KeepGoing132/K4-L3L4-Track2-Day21-Nguyen_Ngoc_Bao-2A202602951-CI-CD-for-AI-Systems/actions/runs/37606981690): chặn model F1 0.6051, giữ nguyên model S3.
- [x] DVC data và model đã có trên Amazon S3; API EC2 được kiểm tra từ IP công khai.
- [x] [Báo cáo](bao-cao.md) hoàn chỉnh; nội dung vừa một trang A4 với Arial 11pt, lề 16mm.
- [x] Đủ chuỗi ảnh 01–05 và ảnh chứng minh Quality Gate; mỗi ảnh dưới 1 MB.
- [x] Code, báo cáo và toàn bộ ảnh đã push lên GitHub.
- [x] Kiểm tra truy cập repository và bằng chứng không cần đăng nhập GitHub.
- [ ] Dán URL repository vào bài Day 21 trên https://vlearn.dev (chưa có phiên đăng nhập VLearn để thực hiện).

## Các ảnh đã nộp

| File | Bằng chứng |
|---|---|
| [01-mlflow-ui.png](anh-chup-man-hinh/01-mlflow-ui.png) | Thí nghiệm MLflow, tham số, F1 và accuracy |
| [02-actions-buoc-2.png](anh-chup-man-hinh/02-actions-buoc-2.png) | Bốn job xanh ở bước 2 |
| [03-actions-buoc-3.png](anh-chup-man-hinh/03-actions-buoc-3.png) | Commit dữ liệu kích hoạt workflow, bốn job xanh |
| [04-curl-api.png](anh-chup-man-hinh/04-curl-api.png) | Terminal thật gọi health và score trên EC2 |
| [05-cloud-storage.png](anh-chup-man-hinh/05-cloud-storage.png) | Bucket S3 có `dvc/` và `artifacts/` |
| [05a-storage-dvc.png](anh-chup-man-hinh/05a-storage-dvc.png) | Các phiên bản dữ liệu trong DVC cache |
| [05b-storage-model.png](anh-chup-man-hinh/05b-storage-model.png) | Model và report tại `artifacts/current/` |
| [07-quality-gate-chan.png](anh-chup-man-hinh/07-quality-gate-chan.png) | Quality Gate fail, Release skipped đúng chủ đích |

Ảnh trình duyệt có thanh địa chỉ. Các ảnh là ảnh chụp trang/terminal đang chạy thực tế.
Kết quả cloud đầy đủ: [ket-qua-cloud.json](ket-qua-cloud.json).
Kết quả local trước triển khai: [ket-qua-local.json](ket-qua-local.json).
Hướng dẫn AWS và cách dừng tài nguyên sau khi chấm: [tasks/aws.md](../tasks/aws.md).

API đang hoạt động: http://54.253.158.211:8080/healthz.
EC2, EBS và IPv4 công khai được giữ để chấm bài và có thể phát sinh phí.
