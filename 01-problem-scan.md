# 01-problem-scan.md

## Phase 1 — SCAN

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | Xanh SM | Lặp lại | Phân bổ lại cuốc xe khi khách đổi điểm đón/trả giữa chừng. |
| 2 | Xanh SM | Tốn thời gian | Điều phối viên xử lý thủ công báo cáo sự cố pin và soạn tin nhắn hướng dẫn. |
| 3 | Xanh SM | Pain từ người khác | Tài xế chờ quá lâu vì hệ thống chưa tự động gợi ý trạm sạc gần nhất hoặc xe cứu hộ khi pin thấp. |
| 4 | VinFast | AI-upgrade | Hệ thống phản hồi sự cố sạc cho khách hàng còn chậm và thiếu cá nhân hóa. |
| 5 | Vinhomes | Tốn thời gian | Nhân viên phải tóm tắt thủ công các phản ánh cư dân và chuyển cho bộ phận xử lý. |

## Phase 2 — QUICK-ASSESS

### Quick Problem Card #1 — Xử lý sự cố sạc pin thực địa
- Bài toán: Tài xế Xanh SM báo hết pin giữa đường cần được điều phối trạm sạc gần nhất hoặc xe cứu hộ.
- Công ty thành viên: Xanh SM
- Ai đang đau? Tài xế và điều phối viên.
- Workflow thủ công hiện tại: tài xế gọi tổng đài → điều phối viên tra cứu vị trí → tra cứu trạm sạc gần nhất → soạn tin nhắn → gọi xe cứu hộ nếu pin thấp.
- Bước tốn thời gian/lỗi nhất: tra cứu trạm và soạn tin nhắn (ước tính 10-12 phút/lượt).
- AI có thể giúp ở bước nào: draft nội dung và đề xuất trạm phù hợp.
- Metric thành công: giảm thời gian xử lý từ 15 phút xuống dưới 3 phút.
- Quick Architecture: LLM

### Quick Problem Card #2 — Tự động hóa phản hồi hủy chuyến
- Bài toán: Tóm tắt lý do khách hàng hủy chuyến từ ghi chú và cuộc gọi.
- Công ty thành viên: Xanh SM
- Ai đang đau? Điều phối viên và bộ phận vận hành.
- Workflow thủ công hiện tại: nhận ghi chú → nghe/đọc log cuộc gọi → tóm tắt nguyên nhân → gửi báo cáo.
- Bước tốn thời gian/lỗi nhất: bước tóm tắt và phân loại nguyên nhân (8-10 phút/lượt).
- AI có thể giúp ở bước nào: tóm tắt và phân loại nguyên nhân.
- Metric thành công: giảm thời gian xử lý từ 10 phút xuống dưới 3 phút.
- Quick Architecture: Rule

### Quick Problem Card #3 — Tự động phân bổ lại cuốc xe
- Bài toán: Khi khách đổi điểm đón/trả giữa chừng, điều phối viên phải tìm lại xe phù hợp.
- Công ty thành viên: Xanh SM
- Ai đang đau? Điều phối viên và tài xế.
- Workflow thủ công hiện tại: nhận yêu cầu → tra cứu xe gần khu vực mới → so sánh lộ trình cũ và mới → gửi thông tin cho tài xế và khách.
- Bước tốn thời gian/lỗi nhất: tra cứu xe và so sánh lộ trình (7-8 phút/lượt).
- AI có thể giúp ở bước nào: đề xuất xe và lộ trình mới.
- Metric thành công: giảm thời gian xử lý từ 8 phút xuống dưới 2 phút.
- Quick Architecture: Rule
