# Triển khai lab trên AWS

**Trạng thái ngày 07/10/2026:** hạ tầng của lần nộp bài đã được xóa theo yêu cầu
dừng phát sinh phí. Workflow đã bị vô hiệu hóa, Secrets/Variables triển khai và
tài khoản CI đã được thu hồi. Hướng dẫn bên dưới mô tả kiến trúc đã kiểm chứng;
cần tạo lại hạ tầng và thông tin xác thực để triển khai lần nữa.
Xem [biên bản dọn AWS](../nop-bai/ket-qua-tat-cloud.json).

Phiên bản này dùng Amazon S3 và EC2 Ubuntu 22.04 tại `ap-southeast-2` (Sydney), vùng
được phép trong tài khoản lab. Hướng dẫn GCP gốc ở `buoc-2.md` chỉ để tham khảo.

## Tài nguyên và quyền

- DVC remote `labstore`: xem `.dvc/config`, prefix `dvc/` trong bucket S3 của bài.
- Model được phát hành tại `artifacts/current/model.joblib`, metrics tại
  `artifacts/current/report.json`.
- EC2 chạy `income-api.service` bằng `/home/ubuntu/income-venv/bin/python`.
- EC2 dùng instance role chỉ có `s3:GetObject` trên `artifacts/current/*`.
- CI dùng IAM user riêng: đọc dữ liệu, ghi artifact và mở/đóng SSH trên đúng security
  group của bài. Key bootstrap trong CSV không được commit hoặc copy lên EC2.
- Cổng 8080 phục vụ API. SSH của mỗi GitHub runner chỉ được mở cho IP `/32` của
  runner và đóng lại ở bước `always()`. Host key được kiểm tra bằng fingerprint.

## GitHub configuration

Repository Secrets: `STORAGE_CREDENTIALS` (JSON có `aws_access_key_id` và
`aws_secret_access_key` của CI user), `ARTIFACT_BUCKET`, `SERVER_HOST`, `SERVER_USER`,
`SERVER_SSH_KEY`.

Repository Variables: `AWS_REGION`, `SECURITY_GROUP_ID`, `SERVER_FINGERPRINT`.

## Luồng chạy

1. Push code lên `main`: Unit Test → Train → Quality Gate → Release.
2. Train dùng `dvc pull`, lưu model ứng viên và báo cáo vào Actions artifacts.
3. F1 lớp dương phải hữu hạn và nằm trong `[0.65, 1]`. Chỉ Release mới upload model
   lên S3, đồng bộ `serve.py`, restart service và kiểm tra health/dự đoán.
4. Bước 3: chạy `python append_batch.py`, `dvc add data/train_batch1.csv`,
   `dvc push`, commit **file `.dvc`** và push để tự động huấn luyện trên 44.722 mẫu.
5. Chứng minh chặn model yếu: chạy workflow thủ công với `quality_gate_demo=true`.
   Pipeline dùng 50 cây, learning rate 0.05, depth 2 trong riêng lần chạy đó;
   nếu F1 dưới 0.65, Release phải ở trạng thái skipped và model S3 không thay đổi.

## Kiểm tra API

Thay `VM_IP` bằng IP trong `nop-bai/ket-qua-cloud.json` sau khi pipeline hoàn tất:

```bash
curl http://VM_IP:8080/healthz
curl -X POST http://VM_IP:8080/score -H 'Content-Type: application/json' \
  -d '{"features": [28, 2, 14, 2, 11, 0, 1, 0, 0, 45]}'
```

## Kết thúc sử dụng

EC2, EBS và địa chỉ IPv4 công khai có thể phát sinh phí. Sau khi chấm bài, dừng hoặc
terminate đúng instance của bài trong EC2 Console; dừng EC2 vẫn giữ EBS. Không xóa
bucket/instance trước khi người chấm kiểm tra API và bằng chứng.

Tham khảo: [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html),
[EC2 instance role](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-metadata-security-credentials.html),
[GitHub AWS credentials action](https://github.com/aws-actions/configure-aws-credentials/tree/v4.3.1).
