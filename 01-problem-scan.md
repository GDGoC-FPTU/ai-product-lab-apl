# 01 — Problem Scan & Quick Cards (Bài cá nhân)

**Lab 02 — AI Product Scoping | Vin Smart Future (Vingroup)**

| Thông tin | Nội dung |
|---|---|
| **Họ và tên** | Đoàn Đình Đông *(sửa lại nếu sai)* |
| **MSSV** | `______________` *(điền trước khi nộp)* |
| **Nhóm** | `______________` *(điền tên nhóm)* |
| **Vai trò giả định** | AI Product Engineer @ Vin Smart Future |
| **Ngày thực hiện** | 24/07/2026 |

> [!NOTE]
> **Ghi chú về số liệu:** Tôi không có quyền truy cập hệ thống BI nội bộ của Vingroup. Toàn bộ con số về thời gian xử lý, volume/ngày và tổn thất trong tài liệu này là **ước lượng phục vụ scoping trong phạm vi Lab**, được suy ra từ mô tả quy trình công khai và giả định vận hành hợp lý. Chúng cần được **xác thực lại bằng log thật** trước khi dùng làm baseline cho bất kỳ quyết định đầu tư nào. Các con số chưa xác thực được đánh dấu `(ước lượng)`.

---

# 🔍 Phase 1 — SCAN: Quét cơ hội bằng 4 Lenses

Tôi quét qua vận hành của 5 công ty thành viên bằng 4 thấu kính: **Lặp lại**, **Tốn thời gian**, **AI-upgrade**, **Pain từ người khác (Stakeholder Pain)**.

### 📝 List bài toán của tôi

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | **Xanh SM (GSM)** | Tốn thời gian | Điều phối viên xử lý thủ công sự cố pin thấp/cạn pin của tài xế giữa ca: tra vị trí xe → tra trụ sạc trống → soạn tin chỉ dẫn → quyết định có gọi cứu hộ hay không. Mất **12–15 phút/lượt** *(ước lượng)*, trong khi tài xế đứng chờ và không thể nhận cuốc. |
| 2 | **VinFast** | Lặp lại | Nhân viên Trung tâm CSKH phân loại & định tuyến thủ công phiếu yêu cầu bảo hành/dịch vụ gửi từ các xưởng ủy quyền (mỗi phiếu là email/form văn xuôi, phải đọc để gán đúng nhóm lỗi + mức ưu tiên + đội kỹ thuật). **~6 phút/phiếu × 250 phiếu/ngày** *(ước lượng)*. |
| 3 | **Vinpearl / VinWonders** | AI-upgrade | Đội Digital Marketing soạn tay phản hồi cho đánh giá của khách trên các nền tảng OTA (Booking, Agoda, TripAdvisor) bằng 3–4 ngôn ngữ. Phản hồi hiện tại chậm (**24–48h**) và rập khuôn copy-paste, làm giảm điểm "Response quality" của khách sạn. |
| 4 | **Vinhomes** | Pain từ người khác | Cư dân phàn nàn rằng ticket gửi qua App Vinhomes Resident bị **chuyển sai phòng ban** (kỹ thuật ↔ vệ sinh ↔ an ninh ↔ tài chính), phải mô tả lại sự việc 2–3 lần. Tỉ lệ định tuyến sai ~**20%** *(ước lượng)*, mỗi lần sai cộng thêm 1 ngày SLA. |
| 5 | **Vinmec** | Tốn thời gian | Bác sĩ điều trị viết tay/gõ tay **tóm tắt hồ sơ xuất viện (discharge summary)** bằng cách đọc lại toàn bộ diễn biến bệnh án. Mất **20–30 phút/bệnh nhân** *(ước lượng)*, thường bị dồn vào cuối ca trực. |
| 6 | **VinFast** | Lặp lại | Kế toán đối soát thủ công hóa đơn sạc điện giữa log phiên sạc của xe và bảng kê của các trạm sạc đối tác (khác định dạng, khác mốc thời gian). Chu kỳ hằng tuần, **~4 giờ/lần** *(ước lượng)*. |

### 🎯 Nhận xét sau khi scan

* Nhóm bài toán **#2, #4, #6** là **phân loại/đối soát có cấu trúc** — đây là vùng mà **rule-based hoặc classifier truyền thống** có thể thắng LLM về chi phí và tính ổn định. Đừng vội gắn LLM vào.
* Nhóm **#1, #3, #5** là **sinh ngôn ngữ tự nhiên từ dữ liệu phân tán** — đây mới đúng "sân" của LLM.
* Bài toán **#5 (Vinmec)** có giá trị cao nhưng **rủi ro lâm sàng/pháp lý nặng nhất** — không phù hợp làm prototype trong 1 buổi Lab.
* Bài toán **#1 (Xanh SM)** là bài duy nhất vừa **real-time**, vừa có **ranh giới an toàn định lượng được** (ngưỡng pin 5%, bán kính 5km) — rất thuận lợi để lập trình và stress-test ranh giới ở Phase 4.

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

Top 3 được chọn từ danh sách SCAN: **#1 (Xanh SM — Sự cố pin)**, **#2 (VinFast — Định tuyến phiếu bảo hành)**, **#3 (Vinpearl — Phản hồi review OTA)**.

## Card #1 — Xanh SM: Xử lý sự cố pin thấp / cạn pin của tài xế giữa ca

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán (1 câu): Điều phối viên phải tra cứu thủ công vị   │
│ trí xe + trụ sạc trống rồi soạn tay tin chỉ dẫn mỗi khi tài │
│ xế báo pin thấp, khiến tài xế chờ lâu và mất cuốc.          │
│ Công ty thành viên: [x] Xanh SM (GSM)                       │
│                                                             │
│ Ai đang đau (Actor)? Điều phối viên tại Trung tâm Điều vận  │
│ (người trực tiếp làm) + Tài xế (người chịu hậu quả chờ đợi) │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Tài xế gọi/nhắn tổng đài báo pin thấp (~2 ph)          │
│ → 2. ĐPV tra định vị GPS xe trên dashboard nội bộ (~2 ph)   │
│ → 3. ĐPV mở app/dashboard trạm sạc tìm trụ trống, đúng       │
│      chuẩn cổng sạc của dòng xe (~5 ph) 🔴                  │
│ → 4. ĐPV soạn tay tin chỉ dẫn đường đi gửi App tài xế (~4 ph)│
│      🔴                                                     │
│ → 5. Nếu pin quá thấp: gọi điều xe sạc di động/cứu hộ (~2 ph)│
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3 + 4 (⏱ 9 phút/lượt) │
│   Nhánh thường (pin ≥5%, B1-B4): ⏱ ~13 phút/lượt (ước lượng)│
│   Nhánh nguy cấp (pin <5%): bỏ qua B3+B4 ⏱ ~8 phút (ướclg)  │
│   (B3+B4 và B5 loại trừ nhau — xem 02-deep-dive-report.md)  │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 3 & 4 — tổng hợp │
│   dữ liệu vị trí + trạm sạc và SOẠN NHÁP tin chỉ dẫn.       │
│   (Bước 5 giữ nguyên cho con người quyết định.)             │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│   1) Đoạn ĐPV thao tác (B2→B4, hiện ~11 phút): p50 xuống    │
│      dưới 4 phút. (Không tính B1 — thời lượng tài xế nói —  │
│      và B5 — thao tác thoại; hai bước này AI không chạm tới)│
│   2) ≥95% bản nháp được ĐPV duyệt-gửi mà không phải sửa lại  │
│      thông tin trạm sạc                                     │
│   3) 100% ca pin <5% được chuyển sang điều xe sạc di động,  │
│      0 ca bị chỉ đến trạm xa hơn 5km                        │
│                                                             │
│ Quick Architecture: [x] LLM Feature (draft + HITL duyệt)     │
│   Không chọn Agent: hành động sai (chỉ xe cạn pin đi xa) gây │
│   hậu quả vật lý ngoài đường, bắt buộc phải có người duyệt.  │
└─────────────────────────────────────────────────────────────┘
```

**Rủi ro chính:** AI chỉ tài xế đến trạm sạc mà xe không đủ pin để tới nơi → xe chết máy giữa đường, phát sinh chi phí cứu hộ + rủi ro an toàn giao thông.
**Ranh giới cần đặt ngay từ prototype:** (1) mọi tin nhắn chỉ là bản nháp có gắn thẻ `[DRAFT_ONLY]`, con người bấm gửi; (2) pin < 5% → cấm đề xuất trạm xa > 5km, bắt buộc chuyển sang điều xe sạc di động.

---

## Card #2 — VinFast: Phân loại & định tuyến phiếu yêu cầu bảo hành từ xưởng dịch vụ

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán (1 câu): Nhân viên CSKH đọc tay từng phiếu yêu cầu │
│ bảo hành viết dạng văn xuôi từ các xưởng ủy quyền để gán     │
│ nhóm lỗi, mức ưu tiên và đội kỹ thuật phụ trách.            │
│ Công ty thành viên: [x] VinFast                             │
│                                                             │
│ Ai đang đau (Actor)? Nhân viên điều phối tại Trung tâm       │
│ Dịch vụ Kỹ thuật VinFast (~250 phiếu/ngày, ước lượng)       │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Nhận phiếu từ email/form của xưởng (mô tả tự do)       │
│ → 2. Đọc & suy luận nhóm lỗi (pin/BMS, phần mềm, thân vỏ,   │
│      điện-điện tử, sạc) (~3 ph) 🔴                          │
│ → 3. Gán mức ưu tiên P1–P3 dựa trên xe có chạy được không   │
│      và xe có thuộc diện triệu hồi không (~2 ph) 🔴         │
│ → 4. Chuyển ticket vào hàng đợi của đội kỹ thuật tương ứng  │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 + 3 (⏱ 5 phút/phiếu)│
│   Tổng quy trình: ⏱ ~6 phút/phiếu (ước lượng)               │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 — trích xuất   │
│   triệu chứng từ văn xuôi thành trường có cấu trúc.         │
│   Bước 3 nên để RULE quyết định, không để LLM.              │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│   1) ≥85% phiếu được gán nhóm lỗi đúng, thời gian < 10 giây │
│   2) Giảm thời gian phân loại từ 6 phút ──> dưới 1,5 phút   │
│   3) 0 phiếu P1 (xe không chạy được) bị hạ xuống P2/P3       │
│                                                             │
│ Quick Architecture: [x] Rule + [x] LLM (hybrid)              │
│   LLM chỉ trích xuất triệu chứng → rule cứng quyết định độ  │
│   ưu tiên và định tuyến. Ưu tiên P1 phải audit được.        │
└─────────────────────────────────────────────────────────────┘
```

**Phản biện (tự stress-test):** Nếu phiếu từ xưởng thực tế đã có **dropdown chọn nhóm lỗi**, thì đây **không phải bài toán AI** — chỉ cần siết validation ở form đầu vào là xong, rẻ hơn nhiều. **Cần kiểm chứng dữ liệu đầu vào thật trước khi làm bất cứ thứ gì.**

---

## Card #3 — Vinpearl / VinWonders: Soạn phản hồi đánh giá của khách trên OTA

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán (1 câu): Đội Digital Marketing soạn tay phản hồi   │
│ cho hàng trăm review đa ngôn ngữ trên Booking/Agoda/        │
│ TripAdvisor, dẫn đến trả lời chậm và nội dung rập khuôn.    │
│ Công ty thành viên: [x] Vinpearl / VinWonders               │
│                                                             │
│ Ai đang đau (Actor)? Chuyên viên Digital Marketing/CSKH của │
│ từng khu nghỉ dưỡng + Khách để lại review không thấy hồi âm │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Tổng hợp review mới từ nhiều kênh OTA (~thủ công)      │
│ → 2. Dịch review tiếng Hàn/Trung/Anh để hiểu nội dung (~3 ph)│
│ → 3. Soạn phản hồi đúng tone thương hiệu, đúng ngôn ngữ gốc │
│      (~8 ph) 🔴                                             │
│ → 4. Quản lý duyệt và đăng lên nền tảng OTA                 │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3 (⏱ 8 phút/review)   │
│   Tổng quy trình: ⏱ ~12 phút/review, SLA hiện tại 24–48h    │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 & 3 — dịch và  │
│   soạn NHÁP phản hồi theo đúng ngôn ngữ gốc của khách.      │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│   1) Giảm thời gian soạn phản hồi từ 12 phút ──> dưới 3 phút│
│   2) Thời gian phản hồi trung bình từ 24–48h ──> dưới 6h    │
│   3) 100% review 1–2 sao phải qua người duyệt trước khi đăng│
│                                                             │
│ Quick Architecture: [x] LLM Feature (draft + HITL duyệt)     │
│   Ranh giới: cấm AI hứa hoàn tiền/bồi thường/nâng hạng       │
│   phòng; cấm nhắc tên nhân viên bị khách phàn nàn.          │
└─────────────────────────────────────────────────────────────┘
```

**Rủi ro chính:** Đây là nội dung **công khai, gắn thương hiệu**. Một phản hồi AI hứa sai (ví dụ tự ý hứa hoàn tiền) sẽ trở thành cam kết công khai không thể rút lại → bắt buộc HITL với review tiêu cực.

---

# 🗳️ Xếp hạng & đề xuất mang vào Deep-Dive nhóm

| Tiêu chí | Card #1 (Xanh SM) | Card #2 (VinFast) | Card #3 (Vinpearl) |
|---|---|---|---|
| Bài toán đủ hẹp để scope trong 1 buổi | ✅ Cao | 🟡 Trung bình | ✅ Cao |
| Metric định lượng rõ ràng | ✅ Có (11 ph → dưới 4 ph, đoạn B2→B4) | ✅ Có (85% / 10s) | ✅ Có (24h → 6h) |
| Ranh giới an toàn lập trình được | ✅ **Rất rõ** (5% pin / 5km) | 🟡 Mơ hồ hơn | 🟡 Phụ thuộc tone |
| LLM có thực sự hơn rule-based? | ✅ Có (sinh ngôn ngữ + tổng hợp) | ❌ Rule có thể thắng | ✅ Có (đa ngôn ngữ) |
| Rủi ro khi AI sai | 🔴 Cao (an toàn) → nhưng chặn được bằng HITL | 🟡 Trung bình | 🔴 Cao (công khai) |

**Đề xuất của tôi cho nhóm: chọn Card #1 (Xanh SM — Sự cố pin thực địa).**
Lý do: đây là bài toán duy nhất có **ranh giới an toàn định lượng được thành mã** (ngưỡng pin `5%`, bán kính `5km`, thẻ `[DRAFT_ONLY]`), nên có thể chứng minh tính khả thi **ngay trong Phase 4** bằng adversarial test thay vì chỉ lập luận trên giấy.

**Lý do loại:**
* **Card #2:** nghi ngờ rule-based/classifier truyền thống rẻ và ổn định hơn LLM; cần kiểm chứng form đầu vào trước — chưa đủ bằng chứng để GO.
* **Card #3:** giá trị rõ nhưng là tác vụ back-office không real-time, và rủi ro thương hiệu khi sai nằm ngoài tầm kiểm soát của một prototype 1 buổi.

---

## 🔗 Liên kết sang các phần sau

* Deep-Dive của nhóm cho bài toán đã chọn: [02-deep-dive-report.md](02-deep-dive-report.md)
* Prototype ranh giới bằng Gemini 2.5 Flash: [starter-code/prompt_prototype.py](starter-code/prompt_prototype.py)
* Nhật ký làm việc với AI: [03-ai-log.md](03-ai-log.md)
