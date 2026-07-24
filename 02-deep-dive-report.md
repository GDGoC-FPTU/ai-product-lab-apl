# 02-deep-dive-report.md

## Quyết định lựa chọn
Nhóm chọn bài toán "Xử lý sự cố sạc pin thực địa" cho Xanh SM.

## Problem Statement (6-field)
| Field | Nội dung |
|---|---|
| Actor / Operator | Điều phối viên (Dispatcher) thuộc Trung tâm Điều vận Xanh SM. |
| Current Workflow | Khi tài xế báo hết pin, điều phối viên tra cứu vị trí định vị, mở dashboard trạm sạc, tìm trụ gần nhất, soạn tin nhắn chỉ dẫn và gọi cứu hộ nếu cần. |
| Bottleneck | Bước tra cứu trạm và soạn tin nhắn mất khoảng 10 phút/lượt, dễ sai và chậm vào giờ cao điểm. |
| Business Impact | Mỗi ngày có nhiều cuộc gọi sự cố pin, làm tăng thời gian chờ đợi của tài xế và ảnh hưởng tới doanh thu và trải nghiệm khách hàng. |
| Success Metric | Giảm thời gian xử lý từ 15 phút xuống dưới 3 phút; đạt tỷ lệ gợi ý đúng hơn 95%. |
| Operational Boundary | AI được phép draft chỉ dẫn và đề xuất trạm sạc, nhưng không tự động gửi tin mà không có duyệt; không đề xuất trạm xa khi pin dưới 5%. |

## Future-State Flow & AI Fit
- AI Fit: LLM Feature.
- Future-State Flow:
  1. Nhận cuộc gọi sự cố từ tài xế.
  2. AI tự động thu thập vị trí và đề xuất trạm sạc gần nhất.
  3. AI draft một tin nhắn chỉ dẫn theo mẫu chuẩn.
  4. Dispatcher duyệt và gửi tin cho tài xế.
  5. Fallback: nếu AI không chắc chắn, điều phối viên tự viết lại như cũ.

## Evaluate
- Checklist: có dữ liệu mẫu, rủi ro có thể kiểm soát qua human-in-the-loop, stakeholders sẵn sàng thay đổi quy trình.
- Quyết định cuối cùng: GO.
- Lý do: bài toán cụ thể, metric rõ ràng, chi phí phát triển thấp và rủi ro có thể kiểm soát bằng HITL và fallback.
