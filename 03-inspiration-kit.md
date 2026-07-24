# Inspiration Kit — Gợi ý tìm bài toán (Vin Smart Future Edition)

> **Sử dụng khi bạn chưa nghĩ ra đủ 5 problems trong Phase 1. Đây không phải kịch bản bắt buộc — chỉ là gợi ý thực tế để kích hoạt tư duy sáng tạo của bạn.**

---

## 🏛️ Gợi ý theo các công ty thành viên Vingroup

Dưới đây là các bài toán thực tế mà bạn có thể dùng để scoping cho bài lab. Mục tiêu là chọn một bài toán mà bạn hiểu rõ quy trình hiện tại và có thể vẽ được ranh giới AI hợp lý.

### 🚗 1. Mảng Ô Tô & Di Chuyển Xanh (VinFast & Xanh SM)

| # | Subsidiary | Tên bài toán / Bottleneck | Lens | Mô tả ngắn |
|---|------------|---------------------------|------|------------|
| 1 | **Xanh SM** | Điều vận thông minh | Tốn thời gian | Tối ưu hóa điểm đón xe dựa trên tin nhắn tài xế và vị trí GPS. |
| 2 | **VinFast** | Hướng dẫn trạm sạc thông minh | AI có thể tốt hơn | Đề xuất trạm sạc phù hợp với loại xe và trạng thái sạc hiện tại. |
| 3 | **VinFast** | Đối chiếu hóa đơn sạc điện | Lặp lại | So khớp dữ liệu sạc từ hàng nghìn trụ với hóa đơn thực tế. |
| 4 | **Xanh SM** | Phân loại lý do hủy chuyến | Pain từ người khác | Tự động phân loại nguyên nhân khách hủy chuyến từ ghi âm và ghi chú. |
| 5 | **VinFast** | Chẩn đoán lỗi xe từ tiếng Việt | AI có thể tốt hơn | Phân loại lỗi xe ban đầu từ mô tả của khách hàng. |

### 🏢 2. Mảng Đô Thị & Quản Lý Vận Hành (Vinhomes & Vinpearl)

| # | Subsidiary | Tên bài toán / Bottleneck | Lens | Mô tả ngắn |
|---|------------|---------------------------|------|------------|
| 6 | **Vinhomes** | Phân loại phản ánh cư dân | Lặp lại | Phân loại khiếu nại gửi qua App đến đúng bộ phận xử lý. |
| 7 | **Vinhomes** | Trợ lý cư dân ảo | AI có thể tốt hơn | Hỗ trợ cư dân tra cứu thủ tục hành chính và draft giấy tờ nhanh. |
| 8 | **Vinpearl** | Tổng hợp review khách sạn | Pain từ người khác | Lọc các review nghiêm trọng để gửi về quản lý kịp thời. |
| 9 | **Vinpearl** | Kiểm tra phòng trống & booking | Tốn thời gian | Đọc email đặt phòng phức tạp và draft lệnh book tự động. |

### 🏥 3. Mảng Y Tế & Giáo Dục (Vinmec & VinUni)

| # | Subsidiary | Tên bài toán / Bottleneck | Lens | Mô tả ngắn |
|---|------------|---------------------------|------|------------|
| 10 | **Vinmec** | Tóm tắt hồ sơ xuất viện | Tốn thời gian | Tự động soạn bản tóm tắt bệnh án cho bác sĩ và bệnh nhân. |
| 11 | **Vinmec** | Phân loại lịch hẹn khám | Pain từ người khác | Gợi ý chuyên khoa phù hợp từ mô tả triệu chứng của khách hàng. |
| 12 | **VinUni** | Chấm điểm và phản hồi bài lab | Lặp lại | Dùng LLM để draft phản hồi học tập cho bài tập code. |

---

## 💡 Lưu ý khi chọn bài toán

1. **Chọn bài toán bạn hiểu rõ nhất.** Ưu tiên bài toán mà nhóm bạn hiểu quy trình hiện tại.
2. **Ranh giới AI rất quan trọng.** Với các mảng nhạy cảm như y tế hoặc an toàn xe, cần có Human-in-the-loop.
3. **Problem First, AI Second.** Đừng chọn bài toán quá phức tạp chỉ để dùng multi-agent. Một giải pháp rule-based hoặc LLM feature đơn giản thường hiệu quả hơn.
