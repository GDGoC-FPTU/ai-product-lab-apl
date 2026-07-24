# 01 — Problem Scan & Quick Cards (Bài cá nhân)

> **Cá nhân:** Phan Bá Khánh Linh — 2A202601989  
> **Ngày thực hiện:** 24/07/2026

## 🔍 Phase 1 — SCAN: Quét cơ hội AI tại Vingroup

Sử dụng 4 lenses để tìm các pain point vận hành thực tế tại các công ty thành viên Vingroup, nơi AI có thể tạo giá trị rõ rệt.

> **Lưu ý:** Các thời lượng và metric dưới đây là giả định để scoping. Cần đo lại bằng log vận hành trước khi pilot; đây không phải số liệu công bố của Vingroup.

### 📝 List bài toán của tôi

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---:|---|---|---|
| 1 | **Vinhomes** | Pain từ stakeholder | Cư dân gửi phản ánh rò nước, thang máy, điện, an ninh bằng văn bản/ảnh/ghi âm; CSKH tự đọc, hỏi lại và chuyển đội. Chậm vài phút ở ca có nguy cơ có thể làm tăng thiệt hại; sai tuyến làm trượt SLA. |
| 2 | **Vinmec** | Tốn thời gian | Điều dưỡng đọc ghi chú chuyển ca dài để tìm cảnh báo, việc chưa hoàn thành và mốc theo dõi. Có thông tin nhạy cảm nên chỉ phù hợp với bản tóm tắt có bác sĩ/điều dưỡng duyệt. |
| 3 | **VinFast** | Lặp lại | Nhân viên bảo hành đọc mô tả lỗi tự do để chọn nhóm lỗi, mức ưu tiên và tài liệu kiểm tra ban đầu. Có thể giảm thời gian tạo phiếu nhưng AI không được kết luận nguyên nhân kỹ thuật. |
| 4 | **Vinpearl / VinWonders** | AI có thể tốt hơn | Nhân viên đọc nhiều đánh giá tiêu cực để tìm chủ đề lặp lại và soạn brief cho quản lý điểm đến. LLM phù hợp để gom chủ đề; số liệu và quyết định khuyến mại cần rule/người duyệt. |
| 5 | **Xanh SM** | Tốn thời gian | Tổng đài tóm tắt hội thoại báo mất đồ/va chạm để tạo case và phân luồng cho supervisor. Cần ẩn PII, không được tự kết luận trách nhiệm hay tự liên hệ khách hàng. |
| 6 | **Vinhomes** | Lặp lại | Ban quản lý rà ticket quá SLA để tìm ticket thiếu ảnh, thiếu vị trí hoặc chuyển sai đội. Có thể tạo danh sách “cần bổ sung”; không tự đóng/mở hoặc đổi SLA. |

## 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

Chọn top 3 bài toán tiềm năng nhất: **#1 (Vinhomes — chuẩn hóa và phân luồng phản ánh sự cố), #2 (VinFast — trợ lý intake bảo hành), #3 (Vinpearl / VinWonders — brief voice of guest).**

### Quick Problem Card #1 — Vinhomes: Chuẩn hóa & phân luồng phản ánh sự cố tòa nhà

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                                        │
│                                                                              │
│ Bài toán: Biến phản ánh tự do của cư dân thành bản nháp ticket có loại sự │
│ cố, mức khẩn, bằng chứng còn thiếu và đội nhận phù hợp để CSKH duyệt.      │
│                                                                              │
│ Công ty thành viên: [x] Vinhomes                                             │
│                                                                              │
│ Ai đang đau (Actor)? Nhân viên CSKH trực ca và trưởng ca vận hành tòa nhà. │
│                                                                              │
│ Workflow thủ công hiện tại (4 bước):                                        │
│   1. Cư dân gửi chat/cuộc gọi/ảnh vào ứng dụng hoặc hotline                 │
│   ──> 2. CSKH đọc-nghe, dò block/căn và hỏi lại thông tin thiếu            │
│   ──> 3. CSKH tự đánh giá mức khẩn, chọn đội kỹ thuật/an ninh/vệ sinh      │
│   ──> 4. CSKH tạo ticket, chuyển giao cho đội hiện trường và theo dõi       │
│           phản hồi                                                           │
│                                                                              │
│ Bước nào tốn thời gian/lỗi nhất? Diễn giải nội dung tự do, hỏi lại và      │
│ chọn đội xử lý (⏱ khoảng 3–6 phút/case). Ca rò nước gần điện hoặc mùi      │
│ khét đặc biệt dễ bị đánh giá không nhất quán.                               │
│                                                                              │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Trích xuất dữ kiện trong case, đề    │
│ xuất nhãn/mức khẩn/đội nhận, nêu dữ kiện thiếu và soạn draft ticket. Rule  │
│ an toàn ép escalation với cháy, khói, điện giật, rò gas, nước gần điện.    │
│                                                                              │
│ Đo thành công bằng gì (Metric có số)? ≥85% draft được CSKH chấp nhận hoặc │
│ sửa nhẹ; ≥90% draft xuất hiện ≤20 giây; giảm median tạo ticket từ baseline │
│ (mục tiêu giả định 4 phút) xuống ≤1,5 phút; 100% case có cờ nguy hiểm được │
│ bắt buộc review trước khi chuyển đội.                                        │
│                                                                              │
│ Quick Architecture: [x] Rule + LLM Feature                                  │
│ Rules kiểm soát escalation/routing/quyền; LLM chỉ cấu trúc ngôn ngữ chưa   │
│ chuẩn. Không phải agent.                                                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Quick Problem Card #2 — VinFast: Trợ lý intake bảo hành từ mô tả lỗi tự do

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                                        │
│                                                                              │
│ Bài toán: Tạo bản nháp phiếu tiếp nhận bảo hành nhất quán từ mô tả của     │
│ khách hàng và lịch sử dịch vụ được cấp quyền.                                │
│                                                                              │
│ Công ty thành viên: [x] VinFast                                              │
│                                                                              │
│ Ai đang đau (Actor)? Cố vấn dịch vụ tại xưởng.                               │
│                                                                              │
│ Workflow thủ công hiện tại (5 bước):                                        │
│   1. Khách mô tả lỗi                                                        │
│   ──> 2. Cố vấn hỏi triệu chứng/bối cảnh                                    │
│   ──> 3. Đọc lịch sử dịch vụ                                                │
│   ──> 4. Chọn nhóm lỗi                                                      │
│   ──> 5. Đặt lịch/ghi chú cho kỹ thuật viên                                 │
│                                                                              │
│ Bước nào tốn thời gian/lỗi nhất? Chuẩn hóa cách diễn đạt (“xe rung”,      │
│ “kêu lạ”) và hỏi đủ dữ kiện (⏱ 5–8 phút/lượt). Thiếu dữ kiện khiến kỹ      │
│ thuật viên phải hỏi lại.                                                     │
│                                                                              │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Gợi ý các câu hỏi làm rõ theo thứ tự │
│ và draft phiếu; rule nhận diện cảnh báo an toàn để yêu cầu dừng sử dụng/    │
│ đưa xe đến nơi an toàn theo SOP đã phê duyệt.                                │
│                                                                              │
│ Đo thành công bằng gì (Metric có số)? ≥80% phiếu có đủ trường bắt buộc     │
│ ngay lần đầu; giảm thời gian intake 6 phút ──> ≤3 phút; 0 chẩn đoán hoặc   │
│ báo giá được AI tự tạo.                                                      │
│                                                                              │
│ Quick Architecture: [x] LLM Feature + Form-validation Rule                  │
│ Không dùng agent và không tự đặt lịch.                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Quick Problem Card #3 — Vinpearl / VinWonders: Brief “Voice of Guest” theo ngày

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                                        │
│                                                                              │
│ Bài toán: Tổng hợp đánh giá và phản hồi khách thành brief theo chủ đề,     │
│ mức ảnh hưởng và ví dụ đại diện để quản lý ưu tiên khắc phục.               │
│                                                                              │
│ Công ty thành viên: [x] Vinpearl / VinWonders                                │
│                                                                              │
│ Ai đang đau (Actor)? Quản lý trải nghiệm khách hàng và nhân viên phân tích │
│ phản hồi.                                                                    │
│                                                                              │
│ Workflow thủ công hiện tại (5 bước):                                        │
│   1. Xuất đánh giá                                                          │
│   ──> 2. Đọc từng phản hồi                                                   │
│   ──> 3. Gắn tag trên bảng tính                                              │
│   ──> 4. Đếm chủ đề, viết email báo cáo                                     │
│   ──> 5. Họp xác nhận hành động                                              │
│                                                                              │
│ Bước nào tốn thời gian/lỗi nhất? Gắn tag thủ công cho phản hồi đa ngôn ngữ │
│ (⏱ 2–3 giờ/ngày ở ngày cao điểm); các chủ đề nhỏ nhưng nghiêm trọng có thể │
│ chìm trong tổng hợp.                                                         │
│                                                                              │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Gom cụm chủ đề, tạo tóm tắt có trích │
│ dẫn ID nội bộ và chỉ ra tín hiệu bất thường; dashboard tính số lượng bằng  │
│ dữ liệu/rule, không để LLM tự bịa số.                                        │
│                                                                              │
│ Đo thành công bằng gì (Metric có số)? Giảm thời gian lập brief 150 phút   │
│ ──> ≤45 phút/ngày; precision top-5 chủ đề ≥85% theo mẫu gán nhãn của nhân │
│ viên; 100% số liệu trong brief truy vết được về ID phản hồi.                │
│                                                                              │
│ Quick Architecture: [x] LLM Feature + Analytics Rule                        │
│ Human review trước khi chia sẻ.                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## ✅ Lý do lựa chọn Top 3

| # | Bài toán | Lý do chọn |
|---:|---|---|
| #1 ✅ | **Vinhomes — Incident Triage Copilot** | **Chọn làm bài nhóm.** Tần suất cao, đầu vào ngôn ngữ không chuẩn nhưng đầu ra có cấu trúc. AI giúp giảm thời gian tạo ticket và hạn chế sai tuyến; phần có hệ quả vận hành được khóa bằng rule và người duyệt. |
| #2 ✅ | VinFast — trợ lý intake bảo hành | Có giá trị trong chuẩn hóa mô tả lỗi và câu hỏi làm rõ; tuy nhiên không để AI chẩn đoán nguyên nhân kỹ thuật, báo giá hoặc tự đặt lịch. |
| #3 ✅ | Vinpearl / VinWonders — brief voice of guest | Hợp với tác vụ gom chủ đề/tóm tắt phản hồi đa ngôn ngữ; số liệu phải truy vết từ ID nội bộ và có human review. |

### Quyết định đề xuất cho nhóm

Chọn **Card 1 — Vinhomes Incident Triage Copilot**. Khác với dự đoán pin, đề xuất này không cần mô hình dự báo lịch sử phức tạp: AI được dùng đúng thế mạnh là hiểu và tóm tắt ngôn ngữ, còn rule và con người giữ các quyết định có hệ quả vận hành.
