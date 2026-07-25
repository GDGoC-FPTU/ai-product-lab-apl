# Lab 02 — Báo cáo nhóm: Deep-Dive Report (Phase 3 + Phase 5)

## Khai báo nhóm

- Tên nhóm: apl
- Vai trò: AI Product Engineer @ Vin Smart Future
- Bài toán nhóm chọn Deep-Dive: Xanh SM (GSM) — Xử lý sự cố hết pin xe điện thực địa

| # | Họ và tên | MSSV | Phần đảm nhận chính |
|---|---|---|---|
| 1 | Lâm Việt Hoàng | _[Điền MSSV]_ | Problem Statement + code prompt prototype |
| 2 | _[Điền họ tên]_ | _[Điền MSSV]_ | Vẽ workflow + Future-State Flow |
| 3 | _[Điền họ tên]_ | _[Điền MSSV]_ | Phần Evaluate + ráp báo cáo |
| 4 | _[Điền họ tên]_ | _[Điền MSSV]_ | AI Log + test ranh giới an toàn |

> Nhóm nhớ sửa lại bảng cho khớp số thành viên thật và điền đúng MSSV từng người trước khi push.

---

## Nhóm đã chốt bài toán nào, và vì sao

Buổi đầu mỗi đứa mang một bài khác nhau vào: có bạn thích bài trích email đặt phòng đoàn của Vinpearl, có bạn muốn làm tóm tắt hồ sơ xuất viện bên Vinmec. Ngồi bàn qua lại một lúc, tụi mình chốt bài xử lý sự cố hết pin thực địa của Xanh SM.

Lý do lớn nhất là bài này đau thật, và đau ngay lúc đó. Tài xế kẹt giữa đường, khách đang chờ, đồng hồ chạy từng phút — cải thiện được là thấy hiệu quả liền, khác với mấy bài back-office để xử lý sau cũng chẳng sao. Thêm nữa, phần AI có thể gánh ở đây rất rõ ràng chứ không mơ hồ: một mặt là tra dữ liệu có cấu trúc (xe đang ở đâu, trạm sạc nào còn trụ trống), mặt kia là viết một đoạn tin nhắn tiếng Việt cho tài xế đọc là hiểu. Vế đầu code thường cũng làm được, nhưng vế sau — viết tự nhiên, đúng giọng — thì đúng chỗ LLM ăn tiền. Và hợp với buổi lab: bài có ranh giới an toàn cụ thể để tụi mình đem đi code rồi thử tấn công (ngưỡng pin 5%, bắt buộc người duyệt trước khi gửi).

Hai bài còn lại tụi mình gác lại chứ không phải không hay. Vinmec dính dữ liệu y tế, sai một chữ là chuyện lớn, không nên đem ra làm thử trong đúng một buổi. Vinpearl thì thú vị nhưng là việc xử lý sau, không gấp bằng chuyện một chiếc xe đang nằm đường.

---

# Phase 3 — DEEP-DIVE

## 3.1. Quy trình hiện tại (Current-State)

Tụi mình ngồi dựng lại từng bước điều phối viên Xanh SM đang làm khi tài xế gọi báo hết pin. Sơ đồ vẽ tay đầy đủ (kèm handoff và bottleneck) nằm ở file `04-workflow-diagram.png`, còn ở đây tóm lại bằng text cho dễ theo dõi:

```text
Bước 1              Bước 2             Bước 3              Bước 4              Bước 5
Nhận cuộc gọi  🔄   Tra định vị GPS    Mở dashboard trạm   Soạn tin hướng  🔄  Gọi đội xe
sự cố từ tài   -->  xe trên bản đồ --> sạc VinFast, lọc --> dẫn đường đi   --> cứu hộ pin
xế (tổng đài)       nội bộ             trụ trống đúng cổng  gửi qua App tài xế  (nếu SoC < 5%)
Dispatcher          Dispatcher         Dispatcher 🔴        Dispatcher 🔴       Dispatcher
~2 phút             ~2 phút            ~5 phút              ~5 phút             ~1 phút

🔴 Bottleneck: Bước 3 + 4 (~10 phút) — ngốn khoảng 2/3 thời gian cả quy trình.
🔄 Handoff: (1) tài xế -> điều phối viên qua tổng đài; (2) điều phối viên -> tài xế qua App.
Tổng thời gian xử lý thủ công: ~15 phút/lượt.
```

Ngồi phân tích thì hai bước 3 và 4 rõ ràng là chỗ nghẽn. Bước 3 điều phối viên phải tự dò trên dashboard trạm sạc xem trụ nào còn trống, mà còn phải để ý đúng loại cổng theo dòng xe (VF5, VFe34, VF8 cổng khác nhau) — dò tay nên vừa lâu vừa dễ chọn nhầm trụ không cắm được. Bước 4 thì phải gõ tay đoạn tin chỉ đường sao cho tài xế đọc hiểu, mỗi người viết một kiểu, lúc cao điểm càng cuống càng dễ sót.

## 3.2. Problem Statement (6-field)

| Field | Nội dung |
|---|---|
| 1. Actor / Operator | Điều phối viên (Dispatcher) ở Trung tâm Điều vận Xanh SM. Giờ cao điểm ôm 5–7 ca cùng lúc nên rất dễ ngộp. Người chịu trận theo là tài xế ngoài đường — chờ lâu thì mất cuốc, tụt thu nhập. |
| 2. Current Workflow | Tài xế gọi báo hết pin → điều phối viên tra định vị xe trên bản đồ nội bộ → mở dashboard trạm sạc VinFast lọc trụ trống đúng cổng → gõ tin hướng dẫn gửi qua App → gọi cứu hộ nếu pin dưới 5%. Năm bước, làm tay hết, tầm 15 phút/lượt. Công cụ: bản đồ nội bộ, dashboard trạm sạc, App nhắn tin. |
| 3. Bottleneck | Bước 3 và 4 (~10 phút). Đây là chỗ vừa phải tra dữ liệu (trạm nào trống, đúng cổng không) vừa phải viết tiếng Việt cho ra hồn — nặng nhất trong cả chuỗi. |
| 4. Business Impact | Tụi mình ước chừng khoảng 60–100 ca hết pin/ngày ở Hà Nội (con số này là nội bộ, cần hỏi lại Khối Vận hành để xác minh, chưa có nguồn công khai). Nhân với 15 phút/ca là tốn cỡ 15–25 giờ công điều vận mỗi ngày. Chưa kể tài xế chờ lâu thì bỏ lỡ khách, cao điểm còn kéo tỉ lệ hủy chuyến lên. |
| 5. Success Metric | (1) Kéo thời gian xử lý từ 15 phút xuống dưới 3 phút/ca. (2) Tỉ lệ gợi ý đúng trạm và đúng cổng sạc từ 98% trở lên. (3) Phản hồi tài xế trong vòng 60 giây đạt từ 95% trở lên. |
| 6. Operational Boundary | AI được phép: gọi API vị trí xe, API trạm sạc còn trống, và soạn tin hướng dẫn ở dạng nháp. AI tuyệt đối không được: tự gửi tin cho tài xế khi chưa có người duyệt, gợi ý trạm sai loại cổng, hoặc chỉ trạm xa quá 5km khi pin dưới 5%. Chốt chặn: mọi tin phải qua điều phối viên bấm duyệt mới được gửi. |

## 3.3. Future-State Flow & AI Fit

Trước khi vẽ quy trình mới, tụi mình cãi nhau một chút về chuyện nên xếp bài này vào loại nào trong AI-Fit Matrix:

- [ ] Rule / State-Machine
- [x] LLM Feature
- [ ] Agentic Loop

Rule thuần thì gãy ngay ở khâu viết tin nhắn — ngôn ngữ tự nhiên muôn hình vạn trạng, không thể if-else hết được. Còn Agentic Loop nghe thì oai nhưng tụi mình thấy không cần, mà còn nguy hiểm: quy trình này có khung cố định, và nếu để AI tự quyết tự làm mà chỉ sai trạm thôi là xe có thể nằm luôn giữa đường, kẹt cả giao thông. Nên chốt LLM Feature: AI lo phần nặng, con người giữ nút bấm cuối.

Quy trình tương lai tụi mình hình dung:

```text
Bước 1              Bước 2                Bước 3                 Bước 4
Nhận cuộc gọi  -->  🔵 AI tự kéo vị   -->  🔵 AI draft tin    -->  🟢 Điều phối viên
sự cố (Dispatcher)  trí xe + lọc trạm      hướng dẫn + chọn        đọc, chỉnh nếu cần,
                    sạc trống đúng cổng    trạm phù hợp, gắn        rồi bấm duyệt & gửi
                                           sẵn [DRAFT_ONLY]        (HITL)

🔵 AI Step   🟢 Human Step (HITL)

Chốt an toàn: nếu pin < 5% -> AI tự đổi sang action dispatch_mobile_charger
(gọi xe cứu hộ pin di động), không thèm gợi ý trạm sạc xa.

↩️ Fallback: AI draft lỗi / không chắc / mất kết nối API -> quay về cách cũ,
điều phối viên tự viết tay như trước (15 phút). Thà chậm còn hơn gửi bậy.
```

Nói ngắn gọn: AI gánh đúng hai bước nghẽn (3 và 4), còn con người từ chỗ ngồi gõ cả đoạn thì giờ chỉ liếc lại và bấm duyệt. Nếu chạy trơn thì 15 phút rút xuống dưới 3 phút là hợp lý.

---

# Phase 5 — EVALUATE

## Checklist độ sẵn sàng

| # | Câu hỏi | Nhóm trả lời | Ghi chú |
|---|---|:---:|---|
| 1 | Có sẵn dữ liệu/logs sạch để test chưa? | Có | Log sự cố pin, API vị trí xe và API trạm sạc VinFast đều đã có trong hệ thống. Trích một tuần log ra là test được. |
| 2 | AI sai thì rủi ro có kiểm soát nổi không? | Có | Có người duyệt trước khi gửi, có fallback về tay, cộng ngưỡng pin 5% chặn cứng. Nhiều lớp nên tụi mình thấy yên tâm. |
| 3 | Mọi người có sẵn sàng đổi cách làm cũ không? | Một phần | Điều phối viên thì mừng vì đỡ việc. Nhưng nên chạy thử ở một trung tâm trước, train thao tác bấm duyệt, ổn rồi mới nhân rộng. |

## Chi phí (ước lượng thô)

Mô hình tụi mình định dùng là Gemini 2.5 Flash-Lite — rẻ, mà tác vụ ở đây chỉ là draft tin ngắn nên quá đủ. Tính ra tầm 60–100 ca/ngày, mỗi ca vài nghìn token cả vào lẫn ra, một ngày cỡ 200K token. Tiền token kiểu này nhỏ xíu so với 15–25 giờ công điều vận tiết kiệm được mỗi ngày. Phần tốn thật ra nằm ở công tích hợp ban đầu — nối API vị trí xe, dashboard trạm sạc và cái nút duyệt trên App — nhưng đó là chi phí một lần, không phải trả đều.

## Quyết định cuối cùng

- [x] GO (bắt đầu làm Prototype, scope hẹp)
- [ ] NOT YET
- [ ] NO-GO

Tụi mình chọn GO. Lý do gói gọn trong bốn ý: bài có scope hẹp và rõ (chỉ đụng bước 3–4, không ôm đồm); metric đo được và có mốc so (15 phút xuống dưới 3 phút, đúng cổng ≥ 98%); giải pháp đủ đơn giản — một lần gọi LLM với output có cấu trúc, tụi mình cố tình không phình lên thành multi-agent cho màu mè; và ranh giới an toàn thì kiểm soát được bằng code, đã đem đi test tấn công hẳn hoi trong `prompt_prototype.py`.

Điều kiện kèm theo: chạy pilot ở một trung tâm điều vận (Hà Nội) tầm 2–4 tuần, giữ 100% có người duyệt, theo dõi xem điều phối viên phải sửa lại draft nhiều không. Bao giờ tỉ lệ draft duyệt-không-sửa đạt tầm 90% trở lên và không còn ca nào gợi ý sai cổng sạc thì mới tính chuyện mở rộng.

---

# Phase 4 — Prompt Prototype (ghi chú kèm)

Phần code tụi mình để ở `starter-code/prompt_prototype.py`, chạy bằng Gemini 2.5 Flash-Lite. Hai ranh giới đem đi bảo vệ:

- Rule 1: output nào cũng phải mở đầu bằng `[DRAFT_ONLY]` — để hệ thống không lỡ tay gửi thẳng khi chưa ai duyệt.
- Rule 2: pin dưới 5% thì cấm chỉ trạm xa quá 5km, phải ép sang `dispatch_mobile_charger`.

Tụi mình viết 3 ca tấn công để thử: (1) giả vờ gấp, ép chỉ trạm xa lúc pin 2%; (2) năn nỉ bỏ cái tag `[DRAFT_ONLY]` cho gọn; (3) chơi chiêu "ignore all previous instructions" để lật system prompt. Cả ba dùng để xem ranh giới có thủng không.

> Lưu ý lúc nộp/chấm: phải set biến môi trường `GEMINI_API_KEY` trước khi chạy script, không thì nó thoát lỗi và autograder tính rớt phần code.

---

*(Hết báo cáo nhóm — Phase 3 & Phase 5.)*
