# 02 — Deep-Dive Report: Vinhomes Incident Triage Copilot

## Thông tin nhóm

- **Tên nhóm:** APL
- **Thành viên:** Phan Bá Khánh Linh — 2A202601989
- **Phạm vi thí điểm:** Một tòa nhà, một ca CSKH và các case phản ánh qua kênh chat nội bộ trong 4 tuần. Các số baseline/chi phí dưới đây là giả định scoping, phải được xác minh với vận hành trước quyết định triển khai.

## Quyết định lựa chọn

Nhóm chọn **Vinhomes Incident Triage Copilot**: một copilot tạo **bản nháp** ticket cho phản ánh sự cố tòa nhà. Hệ thống không thay thế CSKH, không chẩn đoán kỹ thuật, không nhắn tin cho cư dân và không điều động đội hiện trường. Mục tiêu là để nhân viên nhìn thấy cùng lúc: dữ kiện đã có, thông tin cần hỏi, mức khẩn được gợi ý, đội nhận gợi ý và lý do.

## Phase 3.1 — Current-State Workflow Mapping

Sơ đồ trực quan nộp kèm: [`04-workflow-diagram.png`](04-workflow-diagram.png). Quy trình hiện tại được đo theo một case phản ánh thông thường; các case khẩn cần escalation theo SOP ngay, không chờ hết thời lượng trung bình.

| Bước | Người/hệ thống | Thời gian giả định | Handoff / nút thắt |
|---|---|---:|---|
| 1. Nhận chat, cuộc gọi, ảnh hoặc ghi âm | Cư dân → CSKH | 0,5 phút | 🔄 Handoff từ cư dân; nội dung thường thiếu block/căn hoặc mô tả không chuẩn. |
| 2. Đọc-nghe và tra căn hộ/ticket cũ | CSKH + CRM | 1,0 phút | Dễ lộ/chép PII nếu nhân viên copy nhiều hơn cần thiết. |
| 3. Hỏi lại dữ kiện và xác định dấu hiệu nguy hiểm | CSKH ↔ cư dân | 1,5 phút | 🔴 Bottleneck: nhiều lượt hỏi lại; nguy cơ đánh giá không đồng nhất đối với nước/điện/khói. |
| 4. Chọn category, priority, đội nhận và tạo ticket | CSKH + ticketing | 1,5 phút | 🔴 Bottleneck: chọn sai đội làm tăng thời gian chuyển vòng. |
| 5. Chuyển ticket, trưởng ca kiểm tra case P1 | CSKH → đội hiện trường/supervisor | 0,5 phút | 🔄 Handoff cần có ngữ cảnh nhất quán. |

**Tổng thời gian tham chiếu: 5 phút/case.** Baseline thật sẽ lấy từ timestamp CRM trong 2 tuần và tách theo loại case, không dùng một giá trị trung bình để đánh giá mọi sự cố.

## Phase 3.2 — Problem Statement (6 fields)

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Nhân viên CSKH trực ca tạo ticket; trưởng ca review các case P1/khẩn; đội kỹ thuật, an ninh hoặc vệ sinh nhận ticket sau khi con người phê duyệt. |
| **2. Current Workflow** | CSKH nhận phản ánh đa kênh, tra cứu case, hỏi lại block/căn/dấu hiệu/sự cố, tự gắn nhãn và mức ưu tiên, rồi tạo ticket trên hệ thống hiện hữu. Dữ liệu đầu vào lẫn tiếng Việt tự do, viết tắt và đôi khi có ảnh/ghi âm. |
| **3. Bottleneck** | Bước hiểu mô tả chưa cấu trúc và biến nó thành ticket đúng loại/đủ dữ kiện. Sai tuyến hoặc thiếu dấu hiệu nguy hiểm kéo dài vòng handoff; case nước gần điện, mùi gas, khói/cháy không thể để AI tự quyết. |
| **4. Business Impact** | Một case thông thường giả định mất 5 phút; ở 100 case/ngày, giảm 3,5 phút/case có thể giải phóng khoảng 350 phút/ngày để CSKH xử lý việc cần người. Giá trị chỉ được xác nhận sau khi đo volume, tỷ lệ re-route và SLA thật; không dùng giả định này làm cam kết tài chính. |
| **5. Success Metric** | (a) ≥85% draft được accept hoặc chỉnh sửa nhẹ trong pilot; (b) P50 từ nhận case đến draft ≤20 giây và P50 tạo ticket ≤1,5 phút so với baseline; (c) routing accuracy ≥90% trên mẫu được supervisor gán nhãn; (d) recall cờ nguy hiểm =100% trên bộ test được thiết kế; (e) 0 ticket do AI tự tạo/gửi. |
| **6. Operational Boundary** | AI chỉ nhận payload của **một case đã được ẩn/giảm PII**, trả JSON draft có `needs_human_review=true`. AI không truy cập CRM ngoài case, không suy luận danh tính, không chẩn đoán nguyên nhân/sửa chữa, không tự đổi priority/SLA, không gửi tin, không gọi đội hiện trường, không đóng ticket. Các dấu hiệu cháy/khói/rò gas/điện giật/nước chạm nguồn điện luôn `escalate_emergency`; supervisor quyết định bước tiếp theo theo SOP. |

## Phase 3.3 — Future-State Flow & AI Fit

```text
1. Cư dân gửi phản ánh / CSKH nhập case
      ↓
2. [HUMAN] CSKH xác minh tối thiểu: tòa/block/căn, kênh liên hệ, consent sử dụng nội dung
      ↓
3. [RULE] Redact PII không cần thiết + nhận diện từ khóa nguy hiểm + kiểm tra trường bắt buộc
      ↓
4. [AI] LLM tạo JSON: facts, category, urgency đề xuất, đội đề xuất,
        câu hỏi cần bổ sung, bản nháp ticket và lý do (không có quyền thực thi)
      ↓
5. Có dấu hiệu nguy hiểm? ─ Có → [RULE] đặt action=escalate_emergency
      │                              → [HUMAN] supervisor xử lý theo SOP/fallback
      │
      └ Không → [HUMAN] CSKH xem, sửa, xác nhận category/priority/đội nhận
                        ↓
6. [HUMAN + hệ thống hiện hữu] CSKH tạo/chuyển ticket; lưu audit log input-redacted,
   draft, thay đổi của người duyệt và kết quả xử lý

↩ Fallback ở bất kỳ lúc nào: LLM timeout/JSON lỗi/thiếu vị trí/confidence thấp
   → form thủ công có checklist → CSKH hoặc supervisor xử lý theo SOP;
   tuyệt đối không tự gửi hay tự dispatch.
```

### AI-Fit Matrix và lựa chọn kiến trúc

| Phần việc | Rule / State machine | LLM feature | Agentic loop | Lựa chọn và lý do |
|---|---:|---:|---:|---|
| Redact trường, validate schema, quyền truy cập | **Có** | Không | Không | Xác định được, cần audit và tái lập. |
| Nhận diện cờ nguy hiểm/ép escalation | **Có** | Có thể gợi ý | Không | Rule bảo thủ là cổng cuối; LLM không được hạ mức khẩn. |
| Tóm tắt phản ánh và tạo câu hỏi làm rõ | Không | **Có** | Không | Ngôn ngữ tự do, đa dạng cách diễn đạt. |
| Gợi ý category/đội nhận | Rule mapping sau LLM | **Có** | Không | LLM đưa gợi ý + lý do, danh mục/đội hợp lệ do rule giới hạn. |
| Tạo/chuyển/đóng ticket, nhắn cư dân | Quyền hệ thống | Không | **Không dùng** | Đây là hành động tác động vận hành, giữ hoàn toàn cho người. |

**Kết luận AI fit:** dùng **Rule + LLM feature**. Không chọn agentic loop: bài toán không cần lập kế hoạch nhiều bước hay tự gọi công cụ; thêm quyền công cụ sẽ làm rủi ro và chi phí kiểm soát lớn hơn lợi ích của pilot.

### Human-in-the-loop, fallback và quan sát

- **HITL bắt buộc:** CSKH xác nhận mọi trường trước khi tạo ticket; supervisor xác nhận mọi `escalate_emergency` và mọi case priority P1.
- **Fallback:** nếu API, OCR/ASR hoặc LLM không phản hồi, hiển thị checklist thủ công (vị trí, nguy hiểm, ảnh, liên hệ) và tiếp tục theo SOP hiện hành. Nếu có dấu hiệu nguy hiểm, alert supervisor theo kênh có sẵn; không phụ thuộc AI.
- **Audit:** chỉ lưu payload đã giảm PII, version prompt/model, draft, cờ rule, quyết định và chỉnh sửa của người duyệt; phân quyền theo vai trò và chính sách lưu giữ được DPO/IT Security phê duyệt.

## Phase 4 — Technical Prompt Prototype

File [`starter-code/prompt_prototype.py`](starter-code/prompt_prototype.py) chạy được cả khi chưa có API key bằng local safety fallback, và dùng Gemini SDK khi có `GEMINI_API_KEY`. Prototype có schema JSON, policy-enforcement sau LLM và 4 adversarial tests:

1. Prompt injection yêu cầu bỏ review và tự điều đội.
2. Báo khói/mùi gas nhưng yêu cầu giảm ưu tiên.
3. Yêu cầu đưa toàn bộ dữ liệu cư dân/ticket khác vào câu trả lời.
4. Case thường thiếu thông tin, kiểm tra AI không bịa dữ kiện.

Các test xác nhận những hành vi cấm có bị chặn hay không; chúng không chứng minh mô hình đạt metric vận hành. Đây là guardrail prototype, không phải hệ thống production.

## Phase 5 — Evaluate

| AI Readiness checklist | Trạng thái | Bằng chứng / hành động trước pilot |
|---|---|---|
| Có dữ liệu mẫu/log sạch để test? | **Chưa** | Cần 2 tuần case đã ẩn PII và được supervisor gán nhãn category/priority/đội; chia train-free evaluation set, gồm cả case nguy hiểm và tiếng Việt viết tắt. |
| Rủi ro khi AI sai có kiểm soát? | **Có điều kiện** | Cổng rule, human review, không có quyền công cụ và fallback thủ công kiểm soát rủi ro; cần kiểm thử red-team, quyền truy cập, retention và SOP escalation trước thử nghiệm thật. |
| Stakeholder sẵn sàng đổi quy trình? | **Có điều kiện** | CSKH/supervisor cần cùng thiết kế taxonomy, checklist và tiêu chí “accept/sửa nhẹ”; pilot shadow mode 1 tuần trước khi draft hiển thị trong UI. |

### Ước lượng pilot hẹp (không phải báo giá)

| Hạng mục | Ước lượng effort | Ràng buộc chi phí |
|---|---:|---|
| Chuẩn hóa taxonomy, redaction, bộ test ẩn danh | 1–2 tuần | Cần owner vận hành và Security phê duyệt dữ liệu. |
| Prototype read-only + UI review + audit | 2 tuần | Không tích hợp quyền tạo/chuyển ticket trong phase này. |
| Shadow mode và đo baseline/quality | 1–2 tuần | Mẫu review thủ công; theo dõi latency, acceptance, routing, emergency recall. |
| API/model | Giới hạn theo ngân sách pilot | Thiết lập quota, timeout, không gửi dữ liệu vượt payload đã duyệt. |

### Quyết định: **NOT YET — chỉ GO cho shadow-mode nội bộ khi đủ điều kiện**

Chưa nên triển khai vận hành rộng vì chưa có bộ dữ liệu ẩn danh, taxonomy được thống nhất và bằng chứng về recall cờ nguy hiểm. Tuy vậy, bài toán đủ hẹp để bắt đầu **shadow mode read-only** sau khi các điều kiện sau được đáp ứng: (1) Security/DPO duyệt data flow; (2) supervisor gán nhãn bộ benchmark; (3) fallback/SOP được diễn tập; (4) red-team không tìm thấy đường tự tạo ticket, tự gửi tin hoặc lộ PII; (5) pilot đạt các success metric trong ít nhất 2 tuần. Nếu routing rule đơn giản đã đạt mục tiêu nhanh hơn trên một category, ưu tiên rule thay vì ép dùng LLM.
