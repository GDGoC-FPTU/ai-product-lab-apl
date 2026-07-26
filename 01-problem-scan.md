# Lab 02 — Bài cá nhân: Problem Scan (Phase 1 + Phase 2)

- Họ và tên: Lâm Việt Hoàng
- MSSV: 
- Nhóm: apl
- Vai trò: AI Product Engineer @ Vin Smart Future

---

## Phase 1 — SCAN

Mình dùng 4 Lenses (Lặp lại / Tốn thời gian / AI-upgrade / Stakeholder Pain) quét qua các công ty thành viên Vingroup. Dưới đây là 6 bài toán mình ghi lại được:

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | VinFast | Lặp lại | Kế toán đối chiếu hóa đơn sạc điện hằng tuần giữa hàng nghìn trụ sạc đối tác với hệ thống tài chính nội bộ. Mất ~6 tiếng/tuần, chủ yếu ngồi copy-paste và match số. |
| 2 | Xanh SM | Tốn thời gian | Điều phối viên xử lý cuộc gọi tài xế báo hết pin giữa đường. Trung bình 15 phút/lượt: tra vị trí xe → tìm trụ sạc trống đúng cổng → soạn tin hướng dẫn. |
| 3 | Vinhomes | AI-upgrade | Phản hồi khiếu nại cư dân trên app Vinhomes Resident hiện rất rập khuôn, mất trung bình 12 tiếng để phân loại đúng ban quản lý tòa nhà tiếp nhận. |
| 4 | Vinmec | Stakeholder Pain | Bác sĩ nội trú than phiền phải soạn Discharge Summary bằng tay cho từng bệnh nhân, mất 20–30 phút/ca, ăn vào thời gian khám bệnh nhân mới. |
| 5 | Vinpearl | Tốn thời gian | Nhân viên Booking đọc email đặt phòng đoàn từ công ty lữ hành, mất 8–12 phút/email để trích xuất thông tin và soạn xác nhận. Cao điểm ~150 email/ngày. |
| 6 | VinFast | Stakeholder Pain | Khách hàng mô tả lỗi xe bằng tiếng Việt kiểu "xe qua gờ giảm tốc kêu cụp cụp", KTV phải hỏi đi hỏi lại nhiều lần mới mã hóa được thành mã lỗi kỹ thuật. |

**Top 3 mình chọn để làm Quick Card** #2 (Xanh SM), #4 (Vinmec), #5 (Vinpearl). Đây là 3 bài toán mình thấy Actor đau rõ nhất, có số liệu ước tính được, và có mảnh việc mà LLM có thể cắn được.

---

## Phase 2 — QUICK-ASSESS (3 Quick Problem Cards)

### Quick Problem Card #1

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán (1 câu): Điều phối viên Xanh SM mất quá lâu để     │
│   xử lý cuộc gọi tài xế báo hết pin giữa đường.             │
│                                                             │
│ Công ty thành viên: [ ] VinFast  [x] Xanh SM  [ ] Vinhomes  │
│                     [ ] Vinmec   [ ] Khác                   │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│   - Chính: Điều phối viên Trung tâm Điều vận Xanh SM        │
│     (quá tải giờ cao điểm, xử lý song song 5–7 case).       │
│   - Phụ: Tài xế thực địa (mất cuốc khách, tụt thu nhập).    │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Nhận call sự cố                                        │
│    ──> 2. Tra vị trí xe trên map nội bộ                     │
│    ──> 3. Mở dashboard trạm sạc, lọc trụ trống + đúng cổng  │
│    ──> 4. Soạn tin hướng dẫn đường đi gửi qua app tài xế    │
│    ──> 5. Gọi đội cứu hộ pin nếu SoC < 5%                   │
│                                                             │
│ Bước tốn thời gian/lỗi nhất: Bước 3 + 4 (⏱ ~10 phút/lượt)   │
│   Lý do: phải check chéo loại cổng (CCS2 vs GBT) đúng theo  │
│   dòng xe, đồng thời soạn tin tiếng Việt tự nhiên.          │
│                                                             │
│ AI có thể nhảy vào ở bước nào?                              │
│   Bước 3 + 4: LLM tự lấy GPS xe → lọc trụ sạc phù hợp →     │
│   sinh tin nhắn hướng dẫn dạng nháp cho điều phối viên      │
│   duyệt 1 click trước khi gửi.                              │
│                                                             │
│ Đo thành công (Metric có số):                               │
│   - Thời gian xử lý: giảm từ 15 phút ──> dưới 3 phút/lượt   │
│   - Tỉ lệ đề xuất đúng cổng sạc: ≥ 98%                      │
│   - SLA phản hồi tài xế trong 60s: ≥ 95%                    │
│                                                             │
│ Quick Architecture:                                         │
│   [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent                   │
│   → LLM Feature: cần sinh ngôn ngữ tự nhiên tiếng Việt +    │
│   tra cứu structured data. Không dùng Agent vì rủi ro an    │
│   toàn (xe hết pin thật) → phải có HITL bắt buộc.           │
└─────────────────────────────────────────────────────────────┘
```

---

### Quick Problem Card #2

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán (1 câu): Bác sĩ nội trú Vinmec mất 20–30 phút/ca   │
│   để soạn bản Tóm tắt hồ sơ xuất viện bằng tay.             │
│                                                             │
│ Công ty thành viên: [ ] VinFast  [ ] Xanh SM  [ ] Vinhomes  │
│                     [x] Vinmec   [ ] Khác                   │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│   - Chính: Bác sĩ nội trú (mất giờ khám vì task hành chính).│
│   - Phụ: Bệnh nhân & người nhà (chờ thủ tục ra viện lâu).   │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Mở EMR, đọc lại toàn bộ hồ sơ điều trị                 │
│    ──> 2. Tra xét nghiệm, CĐHA, ghi chú lâm sàng            │
│    ──> 3. Soạn tóm tắt: phác đồ + đơn thuốc + dặn dò        │
│    ──> 4. Ký duyệt, chuyển điều dưỡng phát cho bệnh nhân    │
│                                                             │
│ Bước tốn thời gian/lỗi nhất: Bước 3 (⏱ ~20 phút/bệnh nhân)  │
│   Lý do: phải diễn giải thuật ngữ y khoa sang ngôn ngữ dễ   │
│   hiểu + tổng hợp từ nhiều nguồn (EMR, LIS, PACS).          │
│                                                             │
│ AI có thể nhảy vào ở bước nào?                              │
│   Bước 3: LLM đọc structured data từ EMR → draft tóm tắt    │
│   theo template chuẩn Vinmec → bác sĩ review & chỉnh.       │
│                                                             │
│ Đo thành công (Metric có số):                               │
│   - Thời gian bác sĩ dành cho task: giảm từ 20 phút ──>     │
│     dưới 5 phút/bệnh nhân (kể cả bước review).              │
│   - 100% bản tóm tắt phải có chữ ký bác sĩ trước khi phát   │
│     (Human-in-the-loop bắt buộc, không compromise).         │
│                                                             │
│ Quick Architecture:                                         │
│   [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent                   │
│   → LLM Feature + HITL cứng. Y tế cực kỳ nhạy cảm, LLM chỉ  │
│   draft, tuyệt đối không thay bác sĩ ra quyết định y khoa.  │
└─────────────────────────────────────────────────────────────┘
```

---

### Quick Problem Card #3

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán (1 câu): Booking Vinpearl mất 8–12 phút/email để   │
│   đọc email đặt phòng đoàn từ công ty lữ hành và soạn xác   │
│   nhận, tắc nghẽn cao điểm ~150 email/ngày.                 │
│                                                             │
│ Công ty thành viên: [ ] VinFast  [ ] Xanh SM  [ ] Vinhomes  │
│                     [ ] Vinmec   [x] Khác: Vinpearl         │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│   - Chính: Nhân viên Booking (kiệt sức, dễ đọc sai số phòng,│
│     bỏ sót yêu cầu đặc biệt kiểu "cần cũi trẻ em").         │
│   - Phụ: Đối tác lữ hành (chờ xác nhận lâu → chuyển đối     │
│     thủ nếu Vinpearl phản hồi chậm).                        │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Mở email đặt phòng, đọc kỹ nội dung                    │
│    ──> 2. Trích xuất tay: số phòng, loại phòng, check-in/   │
│           out, yêu cầu đặc biệt                             │
│    ──> 3. Mở PMS check quỹ phòng trống                      │
│    ──> 4. Soạn email xác nhận/từ chối gửi đối tác           │
│    ──> 5. Cập nhật CRM                                      │
│                                                             │
│ Bước tốn thời gian/lỗi nhất: Bước 2 + 4 (⏱ ~7 phút/email)   │
│   Lý do: email viết ngôn ngữ tự nhiên, đôi khi trộn Việt–   │
│   Anh, bảng số phòng kèm bảng thời gian ─ dễ đọc nhầm.      │
│                                                             │
│ AI có thể nhảy vào ở bước nào?                              │
│   Bước 2: LLM trích thành JSON chuẩn (rooms, room_type,     │
│   dates, notes) → nhân viên chỉ verify.                     │
│   Bước 4: LLM sinh email xác nhận theo template Vinpearl,   │
│   nhân viên duyệt & gửi.                                    │
│                                                             │
│ Đo thành công (Metric có số):                               │
│   - Thời gian xử lý: giảm từ 10 phút ──> dưới 3 phút/email  │
│   - Độ chính xác trích xuất: ≥ 95%                          │
│   - Tỉ lệ hồi âm đối tác trong 30 phút: từ 40% ──> ≥ 90%    │
│                                                             │
│ Quick Architecture:                                         │
│   [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent                   │
│   → LLM Feature. Rule-based sẽ vỡ vì ngôn ngữ tự nhiên đa   │
│   dạng. Không cần Agent vì mỗi email chỉ 1 lượt trích + 1   │
│   lượt draft, over-engineer nếu dùng Agent loop.            │
└─────────────────────────────────────────────────────────────┘
```

---

Sau khi làm 3 card, mình xếp thứ tự ưu tiên:

| Card | Impact | Feasibility | Safety | Ghi chú nhanh |
|---|:---:|:---:|:---:|---|
| #1 Xanh SM sự cố pin | 5/5 | 4/5 | 3/5 | Impact rõ, số liệu đẹp, nhưng rủi ro (xe hết pin thật) → phải HITL. |
| #2 Vinmec xuất viện | 4/5 | 3/5 | 2/5 | Ý nghĩa xã hội cao, nhưng y tế → compliance nặng, chưa phù hợp làm pilot trong 1 lab. |
| #3 Vinpearl booking | 4/5 | 5/5 | 4/5 | Rõ scope, data sẵn (email), rủi ro thấp, dễ demo trong buổi. |

**Lựa chọn:** Card #3 (Vinpearl) làm bài chính.
