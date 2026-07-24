# 03 — AI Log & Reflection

> Cá nhân: **Phan Bá Khánh Linh — 2A202601989**

## AI đã giúp gì

Tôi dùng AI như một thought-partner ở ba thời điểm. Thứ nhất, AI giúp mở rộng danh sách pain point theo 4 lenses thay vì bám ngay vào ý tưởng dự đoán pin. Tôi chọn lại bài toán triage phản ánh tòa nhà vì nó có đầu vào ngôn ngữ tự do, tác vụ lặp lại và một người vận hành có thể duyệt kết quả rất rõ ràng.

Thứ hai, tôi dùng AI để phản biện kiến trúc. Bản brainstorm ban đầu đề xuất một agent có thể đọc CRM, gọi đội kỹ thuật và nhắn cư dân. Khi yêu cầu AI đóng vai trưởng ca và Security reviewer, tôi nhận ra đây là một scope quá rộng: lỗi routing, lộ PII hoặc tự động dispatch đều có hậu quả vận hành. Vì vậy tôi tách rule (permission, cờ nguy hiểm, schema, redaction) ra khỏi LLM (tóm tắt, câu hỏi làm rõ, draft ticket).

Thứ ba, AI hỗ trợ viết adversarial inputs: yêu cầu bỏ human review, hạ priority trong case khói/mùi gas, đòi xuất dữ liệu ticket khác và yêu cầu bịa thông tin căn hộ. Những test này giúp biến boundary thành assertion chạy được thay vì chỉ ghi “hãy an toàn” trong prompt.

## AI đã sai hoặc thiếu gì

AI từng đưa ra các con số như thể Vinhomes có một volume ticket, SLA và hệ thống dữ liệu cụ thể. Đây là **hallucination về bối cảnh doanh nghiệp**: tôi không có quyền khẳng định các số đó. Tôi đổi toàn bộ con số trong bài thành baseline giả định để scoping và nêu cách lấy log xác minh trước pilot.

AI cũng có xu hướng gọi mọi thứ là “agent” và khuyên hệ thống tự tạo ticket để “end-to-end”. Đó không phải là lựa chọn tốt hơn: bài toán chỉ cần hiểu mô tả chưa cấu trúc, trong khi hành động tạo/chuyển ticket có quyền tác động vào vận hành. Một mô hình có thể hiểu sai tiếng Việt viết tắt, ảnh mờ hoặc từ “mùi khét”; vì vậy LLM không được phép làm cổng an toàn cuối cùng.

## Tôi đã sửa prompt và ranh giới thế nào

Tôi đổi system prompt sang output JSON cố định gồm `facts`, `missing_information`, `suggested_category`, `suggested_urgency`, `suggested_team`, `action`, `needs_human_review` và `draft_ticket`. Prompt cấm suy luận dữ kiện không xuất hiện trong case, cấm truy cập/nhắc tới dữ liệu ngoài case, cấm gửi tin và cấm dispatch. Sau output LLM, policy code kiểm tra lại schema, gắn `[DRAFT_ONLY]`, và cưỡng chế `escalate_emergency` khi input có dấu hiệu nguy hiểm.

Tôi cũng thêm fallback cục bộ để script vẫn chạy khi chưa có API key hoặc khi model trả JSON lỗi. Đó không phải cách “lách” mô hình: mục đích là chứng minh guardrail có thể được kiểm thử độc lập. Trong sản phẩm thật, fallback sẽ là form thủ công và SOP của trưởng ca. Sau lần này, tôi hiểu rằng chất lượng một ý tưởng AI không nằm ở việc để AI làm nhiều việc nhất, mà ở việc xác định chính xác nơi AI chỉ nên **gợi ý**, nơi rule phải **chặn**, và nơi con người phải **quyết định**.
