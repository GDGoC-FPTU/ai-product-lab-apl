# 01 — Problem Scan & Quick Cards (Bài cá nhân)

---

## 🔍 Phase 1 — SCAN: Quét cơ hội AI tại Vingroup

Sử dụng **4 Lenses** để tìm kiếm các pain point vận hành thực tế tại các công ty thành viên Vingroup, nơi AI có thể mang lại giá trị rõ rệt.

### 📝 List bài toán của tôi:

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | **Vinmec** | Tốn thời gian | Bác sĩ mất 20–30 phút viết tóm tắt hồ sơ xuất viện (Discharge Summary) cho mỗi bệnh nhân, trích xuất thủ công từ bệnh án điện tử, kết quả xét nghiệm và ghi chú điều trị để soạn bản tóm tắt dễ hiểu cho bệnh nhân mang về. |
| 2 | **VinFast** | AI có thể tốt hơn | Khách hàng gọi hotline/gửi tin nhắn mô tả lỗi xe bằng tiếng Việt tự nhiên (VD: *"xe qua gờ giảm tốc kêu cụp cụp ở bánh trước"*), nhân viên CSKH phải tra cứu thủ công mã lỗi kỹ thuật trong catalog hàng nghìn mã — mất 8–15 phút/vụ và sai sót do hiểu nhầm ngữ nghĩa. |
| 3 | **Vinhomes** | Lặp lại | Mỗi ngày ban quản lý nhận 200–400 phản ánh cư dân qua App Vinhomes Resident (mất nước, hỏng thang máy, ồn ào, phí dịch vụ…). Nhân viên CSKH phải đọc từng tin, phân loại thủ công và chuyển đến đúng bộ phận xử lý — mất trung bình 3–5 phút/phản ánh, thường xuyên chuyển nhầm bộ phận. |
| 4 | **Vinpearl** | Pain từ người khác | Quản lý khách sạn Vinpearl phàn nàn không kịp phát hiện các review tiêu cực khẩn cấp (phòng bẩn, thái độ nhân viên kém) trên Booking.com, Agoda, Google Maps. Nhân viên quét thủ công ~150 review/ngày trên 3–4 nền tảng, phàn nàn khẩn thường bị phát hiện trễ 24–48h dẫn đến mất khách. |
| 5 | **Xanh SM** | Tốn thời gian | Đội vận hành cần phân tích lý do hủy chuyến từ ghi âm cuộc gọi tổng đài và ghi chú tài xế để tìm pattern lỗi hệ thống (VD: định vị sai, app treo, thời gian chờ quá lâu). Hiện nhân viên nghe thủ công từng ghi âm 2–5 phút, ghi chép vào Excel — xử lý 50 case/ngày mất ~4 giờ. |
| 6 | **VinFast** | Lặp lại | Bộ phận tài chính VinFast đối chiếu hàng tuần dữ liệu sạc điện từ hàng nghìn trụ sạc liên kết (đối tác bên ngoài) với hóa đơn thực tế gửi về — so khớp thủ công trên Excel mất 2 ngày/tuần, tỷ lệ sai sót 3–5%. |

---

## 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

Chọn top 3 bài toán tiềm năng nhất: **#1 (Vinmec — Tóm tắt xuất viện), #2 (VinFast — Chẩn đoán lỗi xe), #3 (Vinhomes — Phân loại phản ánh cư dân)**.

---

### Quick Problem Card #1 — Vinmec: Soạn tóm tắt hồ sơ xuất viện

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Bác sĩ Vinmec mất quá nhiều thời gian soạn thảo  │
│ tóm tắt hồ sơ xuất viện (Discharge Summary) cho bệnh nhân  │
│ từ dữ liệu bệnh án điện tử, xét nghiệm và ghi chú điều trị│
│                                                             │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau (Actor)? Bác sĩ điều trị — quá tải hành chính, │
│ mất thời gian khám cho bệnh nhân khác vì phải ngồi soạn    │
│ tóm tắt xuất viện bằng tay.                                │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Bác sĩ mở bệnh án điện tử (EMR), đọc lịch sử điều trị│
│   ──> 2. Mở tab xét nghiệm, tổng hợp các kết quả quan trọng│
│   ──> 3. Đọc lại ghi chú điều trị hằng ngày của mình       │
│   ──> 4. Soạn văn bản tóm tắt xuất viện bằng ngôn ngữ dễ  │
│         hiểu cho bệnh nhân (chẩn đoán, thuốc, lịch tái khám│
│   ──> 5. In và ký xác nhận, giao cho điều dưỡng phát hành  │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 4 (⏱ 15–20 phút/lượt)│
│ — Bác sĩ phải chuyển đổi thuật ngữ y khoa sang ngôn ngữ    │
│ bệnh nhân hiểu được, dễ bỏ sót thông tin thuốc/lịch tái khám│
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2–4             │
│ — AI trích xuất tự động dữ liệu EMR + xét nghiệm, draft   │
│ bản tóm tắt xuất viện bằng ngôn ngữ thân thiện. Bác sĩ chỉ │
│ cần review và ký xác nhận.                                  │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ "Giảm thời gian soạn tóm tắt xuất viện từ 25 phút ──>     │
│ dưới 5 phút/bệnh nhân. Tỷ lệ draft AI được bác sĩ chấp    │
│ nhận không cần sửa lớn đạt ≥ 85%."                          │
│                                                             │
│ Quick Architecture: [x] LLM Feature                        │
│ (Trích xuất + tóm tắt ngôn ngữ tự nhiên từ EMR)            │
└─────────────────────────────────────────────────────────────┘
```

---

### Quick Problem Card #2 — VinFast: Chẩn đoán lỗi xe từ mô tả tiếng Việt

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Khách hàng VinFast mô tả hiện tượng lỗi xe bằng │
│ tiếng Việt tự nhiên, nhân viên CSKH phải tra cứu thủ công  │
│ mã lỗi kỹ thuật trong catalog hàng nghìn mã — chậm và sai  │
│                                                             │
│ Công ty thành viên: [x] VinFast                             │
│                                                             │
│ Ai đang đau (Actor)? Nhân viên CSKH tuyến đầu (Agent) và   │
│ khách hàng (chờ đợi lâu để được hẹn lịch sửa đúng hạng mục)│
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Khách gọi hotline/gửi tin mô tả lỗi bằng ngôn ngữ    │
│      tự nhiên (VD: "xe kêu rít khi đạp phanh lúc trời mưa")│
│   ──> 2. Agent ghi chép lại mô tả vào hệ thống CRM        │
│   ──> 3. Agent tra cứu thủ công catalog mã lỗi kỹ thuật    │
│         (hàng nghìn mã, phân theo hệ thống: phanh, pin,    │
│         treo, điện...) để tìm mã phù hợp nhất              │
│   ──> 4. Agent tạo phiếu hẹn sửa chữa với mã lỗi sơ bộ   │
│   ──> 5. Kỹ sư xưởng nhận phiếu, chẩn đoán lại từ đầu    │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3 (⏱ 8–15 phút/lượt)│
│ — Agent không có nền tảng kỹ thuật, dễ map sai mã lỗi.     │
│ 30–40% phiếu hẹn bị gán sai mã → kỹ sư phải chẩn đoán lại│
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 3               │
│ — LLM phân tích mô tả tiếng Việt, đề xuất top-3 mã lỗi    │
│ kỹ thuật kèm confidence score. Agent chỉ cần xác nhận.     │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ "Giảm thời gian tra cứu mã lỗi từ 12 phút ──> dưới 1 phút.│
│ Tỷ lệ gán đúng mã lỗi sơ bộ tăng từ 60% lên ≥ 90%."      │
│                                                             │
│ Quick Architecture: [x] LLM Feature                        │
│ (NLU tiếng Việt → phân loại mã lỗi kỹ thuật)              │
└─────────────────────────────────────────────────────────────┘
```

---

### Quick Problem Card #3 — Vinhomes: Phân loại & Điều hướng phản ánh cư dân

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Nhân viên CSKH Vinhomes đọc và phân loại thủ công│
│ 200–400 phản ánh cư dân/ngày trên App, thường xuyên chuyển │
│ nhầm bộ phận xử lý khiến thời gian phản hồi kéo dài 12–24h│
│                                                             │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau (Actor)? Nhân viên CSKH ban quản lý tòa nhà    │
│ (đọc tin quá tải) và cư dân (chờ phản hồi quá lâu, phải    │
│ gọi lại nhiều lần vì bị chuyển nhầm bộ phận).              │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Cư dân gửi phản ánh qua App Vinhomes Resident (text,  │
│      ảnh, hoặc ghi âm)                                     │
│   ──> 2. Nhân viên CSKH đọc từng phản ánh, xác định danh   │
│         mục (kỹ thuật/an ninh/vệ sinh/phí dịch vụ/tiếng ồn)│
│   ──> 3. Chuyển phản ánh đến đúng ban quản lý/bộ phận xử lý│
│         của tòa nhà tương ứng                               │
│   ──> 4. Bộ phận tiếp nhận phản hồi cư dân qua App         │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2–3 (⏱ 3–5 phút/lượt)│
│ — Với 300 phản ánh/ngày → mất ~15–25 giờ nhân công/ngày.   │
│ Tỷ lệ chuyển nhầm bộ phận: ~20%, khiến cư dân phải chờ    │
│ thêm 12h nữa để được điều hướng lại.                       │
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2–3             │
│ — LLM đọc nội dung phản ánh (text + caption ảnh), tự động  │
│ phân loại danh mục + xác định tòa nhà + mức độ khẩn cấp,  │
│ draft phản hồi sơ bộ cho cư dân. CSKH chỉ cần duyệt.      │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ "Giảm thời gian phân loại từ 4 phút ──> dưới 10 giây/phản  │
│ ánh. Tỷ lệ điều hướng đúng bộ phận tăng từ 80% lên ≥ 95%. │
│ Thời gian phản hồi trung bình giảm từ 12h xuống dưới 2h."  │
│                                                             │
│ Quick Architecture: [x] LLM Feature                        │
│ (Phân loại văn bản + điều hướng tự động + draft phản hồi)  │
└─────────────────────────────────────────────────────────────┘
```

---

## Lý do lựa chọn Top 3 và loại bỏ các bài toán còn lại:

| # | Bài toán | Lý do chọn / loại |
|---|----------|-------------------|
| **#1 ✅** | Vinmec — Tóm tắt xuất viện | **CHỌN** — Impact cao (bác sĩ tiết kiệm 20 phút/bệnh nhân), LLM xử lý tốt tác vụ trích xuất + tóm tắt ngôn ngữ tự nhiên, dữ liệu EMR có cấu trúc sẵn. |
| **#2 ✅** | VinFast — Chẩn đoán lỗi xe | **CHỌN** — Bài toán NLU tiếng Việt → phân loại kỹ thuật rất phù hợp LLM, catalog mã lỗi có sẵn làm ground truth, metric rõ ràng (accuracy + speed). |
| **#3 ✅** | Vinhomes — Phân loại phản ánh | **CHỌN** — Volume lớn (300+ phản ánh/ngày), tác vụ lặp đi lặp lại, LLM xử lý phân loại text tốt hơn rule-based vì cư dân viết đa dạng ngữ cảnh. |
| #4 ❌ | Vinpearl — Review khách sạn | **LOẠI** — Tác vụ back-office (phân tích offline), không ảnh hưởng trực tiếp đến trải nghiệm khách hàng real-time. Có thể dùng rule-based sentiment analysis đủ tốt. |
| #5 ❌ | Xanh SM — Phân tích hủy chuyến | **LOẠI** — Cần pipeline Speech-to-Text phức tạp trước khi dùng LLM, chi phí triển khai cao, và kết quả chỉ phục vụ báo cáo nội bộ (không cải thiện vận hành real-time). |
| #6 ❌ | VinFast — Đối chiếu hóa đơn sạc | **LOẠI** — Bài toán so khớp dữ liệu có cấu trúc, rule-based matching + fuzzy logic truyền thống có thể giải quyết hiệu quả hơn LLM với chi phí thấp hơn nhiều. |
