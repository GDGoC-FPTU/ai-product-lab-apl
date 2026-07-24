# 02 — Problem Deep-Dive Report & Evaluation (Bài nhóm)

---

## 👥 1. Khai báo thành viên nhóm

* **Tên nhóm:** Vin Smart Future — Team 01
* **Thành viên tham gia:**
  1. Nguyễn Ngọc Tú — MSSV: [Điền MSSV] (Leader / AI Product Engineer)
  2. [Họ và tên thành viên 2] — MSSV: [Điền MSSV]
  3. [Họ và tên thành viên 3] — MSSV: [Điền MSSV]
  4. [Họ và tên thành viên 4] — MSSV: [Điền MSSV]

---

## 🏛️ 2. Quyết định lựa chọn bài toán cho Deep-Dive

Nhóm thống nhất chọn bài toán: **"Xanh SM — Xử lý sự cố hết pin / sạc pin thực địa cho tài xế taxi điện"** (Card #2 từ Phase 2).

### 💡 Lý do lựa chọn bài toán này:
* **Tác động vận hành trực tiếp (Real-time impact):** Mỗi ngày tại Hà Nội và TP.HCM có trung bình 80–120 trường hợp tài xế báo sự cố sắp cạn pin hoặc cạn pin giữa đường. Việc xử lý chậm kéo dài thời gian chờ của tài xế, gây tắc nghẽn giao thông và rò rỉ doanh thu cuốc xe (~15%).
* **Công nghệ vừa đủ (LLM Feature):** Không cần xây dựng Multi-Agent phức tạp hay train model riêng. Giải pháp LLM Feature kết hợp RAG/API lookup nhẹ giúp trích xuất định vị, so khớp trạm sạc trống và draft tin nhắn chỉ đường chuẩn xác trong vài giây.
* **Ranh giới an toàn rõ ràng:** Có thể áp dụng cơ chế **Human-in-the-loop (HITL)** bằng thẻ `[DRAFT_ONLY]` bắt buộc điều phối viên duyệt trước khi gửi, loại bỏ hoàn toàn rủi ro AI gửi nhầm thông tin cho tài xế.

---

# 🏗️ Phase 3 — DEEP-DIVE

## 3.1. Current-State Workflow Mapping (Quy trình thủ công hiện tại)

Sơ đồ trực quan hóa chi tiết được đính kèm tại file [04-workflow-diagram.png](04-workflow-diagram.png).

### 📋 Các bước quy trình thủ công (Tổng thời gian: 15 phút/lượt xử lý):

```text
┌────────────────┐     ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ Bước 1         │     │ Bước 2         │     │ Bước 3         │     │ Bước 4         │
│ Tiếp nhận cuộc │     │ Tra cứu vị trí │     │ Tra cứu trạm   │     │ Soạn thảo tin  │
│ gọi sự cố      │ ──> │ định vị GPS xe │ ──> │ sạc VinFast    │ ──> │ nhắn hướng dẫn │
│                │     │                │     │ còn trụ trống  │     │ gửi tài xế     │
│ Ai: Dispatcher │     │ Ai: Dispatcher │     │ Ai: Dispatcher │     │ Ai: Dispatcher │
│ ⏱ 2 phút       │     │ ⏱ 2 phút       │     │ ⏱ 5 phút 🔴    │     │ ⏱ 5 phút 🔴    │
│ In: Gọi tổng đài│    │ In: Biển số xe │     │ In: Tọa độ GPS │     │ In: Data trạm  │
│ Out: Log sự cố │     │ Out: Tọa độ    │     │ Out: Địa chỉ   │     │ Out: SMS/App   │
└────────────────┘     └────────────────┘     └────────────────┘     └────────────────┘
                                                                              │
                                                                              ▼
                                                                       ┌────────────────┐
                                                                       │ Bước 5         │
                                                                       │ Gọi xe cứu hộ  │
                                                                       │ pin (nếu < 5%) │
                                                                       │ Ai: Dispatcher │
                                                                       │ ⏱ 1 phút       │
                                                                       └────────────────┘
🔴 = Bottlenecks (Nút thắt cổ chai tốn thời gian nhất)
🔄 Handoffs: Chuyển giao thông tin từ Tài xế ➔ Tổng đài ➔ App bản đồ internal ➔ Dashboard trạm sạc VinFast ➔ App Tài xế.
```

### 🔴 Chi tiết các Bottlenecks:
1. **Bước 3 (Tra cứu trạm sạc — 5 phút):** Điều phối viên phải mở tay Dashboard trạm sạc VinFast, lọc theo đúng loại cổng sạc (CCS2 cho VF8/VF9, GBT cho VF5/e34), kiểm tra số trụ trống thời gian thực và đo khoảng cách thủ công trên bản đồ.
2. **Bước 4 (Soạn tin nhắn hướng dẫn — 5 phút):** Điều phối viên gõ tay văn bản hướng dẫn chi tiết đường đi, tên trạm, địa chỉ và lưu ý an toàn gửi qua App tài xế. Dễ xảy ra sai sót gõ nhầm địa chỉ hoặc quên lưu ý pin cực thấp.

---

## 3.2. Problem Statement (6-field Standard)

| Trường thông tin | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Điều phối viên (Dispatcher) thuộc Trung tâm Điều vận Xanh SM (GSM). |
| **2. Current Workflow** | Khi tài xế báo sự cố hết pin/sắp hết pin, điều phối viên mở hệ thống GPS tra cứu tọa độ xe, tra cứu thủ công Dashboard trạm sạc VinFast gần nhất còn trụ trống phù hợp dòng xe, viết tin nhắn chỉ đường gửi qua App tài xế, và gọi đội cứu hộ lưu động nếu pin dưới 5%. Quy trình 5 bước thủ công, tốn 15 phút/lượt. |
| **3. Bottleneck** | **Bước 3 & 4 (mất 10/15 phút):** Tra cứu thủ công trụ sạc khả dụng theo loại cổng xe và gõ tay tin nhắn hướng dẫn tiếng Việt chuẩn xác. |
| **4. Business Impact** | Với ~100 sự cố/ngày tại các thành phố lớn, quy trình lãng phí **25 giờ lao động/ngày** của team điều vận. Thời gian xử lý lâu làm gia tăng áp lực cho tài xế, nguy cơ xe cạn pin dừng giữa đường gây cản trở giao thông và sụt giảm **15% doanh thu cuốc xe** trong thời gian chờ. |
| **5. Success Metric** | **1. Speed:** Giảm tổng thời gian xử lý sự cố từ 15 phút xuống **dưới 3 phút/lượt** (giảm 80%).<br>**2. Quality:** Tỷ lệ gợi ý đúng trạm sạc trống và phù hợp chuẩn cổng sạc đạt **≥ 98%**.<br>**3. Safety:** 100% trường hợp pin dưới 5% được tự động chuyển hướng sang điều động Xe Cứu Hộ Pin Di Động. |
| **6. Operational Boundary** | **AI ĐƯỢC PHÉP:** Lấy dữ liệu GPS xe, tra cứu API trạm sạc VinFast trống, tự động draft tin nhắn chỉ đường kèm vị trí và loại trụ sạc.<br>**TUYỆT ĐỐI CẤM:**<br>1. AI không được gửi tin nhắn trực tiếp cho tài xế mà KHÔNG có phê duyệt của Điều phối viên (Bắt buộc thẻ `[DRAFT_ONLY]`).<br>2. AI không được chỉ dẫn xe có pin < 5% di chuyển đến trạm sạc xa > 5km (bắt buộc kích hoạt `dispatch_mobile_charger`). |

---

## 3.3. Future-State Flow & AI Fit

### 📊 AI-Fit Matrix Assessment:
- [ ] **Rule / State-Machine:** Không đủ linh hoạt vì mô tả sự cố của tài xế và ngữ cảnh vị trí mang tính tự nhiên, cần khả năng tổng hợp thông tin và soạn văn bản thân thiện.
- [x] **LLM Feature (Lựa chọn của nhóm):** Phù hợp nhất! Quy trình có các bước đầu vào/đầu ra cố định. LLM đóng vai trò trích xuất thông tin, kết hợp dữ liệu API và draft văn bản chuẩn xác theo ranh giới an toàn.
- [ ] **Agentic Loop:** Không cần thiết vì quy trình không đòi hỏi tự trị đa bước phức tạp; rủi ro để Agent tự quyết định điều vận xe có thể gây sự cố an toàn giao thông.

### 🔄 Quy trình tương lai (Future-State Workflow):

```text
┌────────────────┐     ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ Bước 1         │     │ Bước 2         │     │ Bước 3         │     │ Bước 4         │
│ Tài xế báo     │ ──> │ 🔵 AI Auto-pull│ ──> │ 🔵 LLM Draft   │ ──> │ 🟢 Dispatcher  │
│ sự cố qua App  │     │ GPS & Tra cứu  │     │ tin chỉ đường  │     │ click Duyệt    │
│ hoặc Tổng đài  │     │ Trạm trống API │     │ kèm [DRAFT]    │     │ & Gửi tài xế   │
└────────────────┘     └────────────────┘     └────────────────┘     └────────────────┘
                                                                              │
                                                                              ▼
                                                                       ↩️ Fallback:
                                                                       Nếu LLM lỗi/API down,
                                                                       hệ thống tự chuyển
                                                                       về màn hình tra cứu
                                                                       thủ công như cũ.
```

* 🔵 **AI Step:** Tự động lấy dữ liệu GPS, tra API trạm sạc VinFast, dùng LLM draft tin nhắn hướng dẫn hoặc trả JSON cứu hộ khẩn cấp.
* 🟢 **Human Step (HITL):** Điều phối viên đọc bản nháp có thẻ `[DRAFT_ONLY]`, kiểm tra nhanh và bấm nút "Gửi".
* ↩️ **Fallback Plan:** Nếu Gemini API gặp lỗi (503/429) hoặc API trạm sạc không phản hồi trong 3 giây, giao diện tự động bật bảng tra cứu thủ công fallback để Điều phối viên xử lý truyền thống, đảm bảo không gián đoạn vận hành.

---

# 🏁 Phase 5 — EVALUATE: Đánh giá độ sẵn sàng & Quyết định

### 📋 AI Readiness Checklist:
1. [x] **Dữ liệu:** VinFast & Xanh SM đã có sẵn API định vị GPS xe điện và API trạng thái trụ sạc VinFast thời gian thực (Real-time API).
2. [x] **Kiểm soát rủi ro:** Rủi ro sai sót được kiểm soát 100% thông qua lớp phê duyệt Human-in-the-loop (HITL) và ranh giới cứng trong System Prompt.
3. [x] **Sẵn sàng vận hành:** Đội ngũ điều phối viên hoan nghênh công cụ trợ lý nháp (Dispatcher Co-Pilot) vì giúp giảm bớt 80% thao tác gõ phím thủ công giờ cao điểm.

### ⚖️ Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future:

**[ x ] GO (Bắt đầu xây dựng sản phẩm Prototype & Pilot)**

### 📝 Justification (Luận chứng kỹ thuật và chi phí):
1. **Khả thi Kỹ thuật (Technical Feasibility):** Thử nghiệm thực tế với `prompt_prototype.py` trên **Gemini 2.5 Flash** chứng minh mô hình tuân thủ nghiêm ngặt ranh giới an toàn: giữ thẻ `[DRAFT_ONLY]` đạt 100% và kích hoạt chính xác `dispatch_mobile_charger` khi pin < 5%.
2. **Hiệu quả Chi phí (Cost Efficiency):** 
   - Chi phí API Gemini 2.5 Flash ước tính: ~$0.0005/lượt xử lý. Với 100 sự cố/ngày ➔ Chi phí AI chỉ khoảng **$1.5 / tháng** (~38.000 VNĐ/tháng).
   - Giá trị mang lại: Tiết kiệm **750 giờ làm việc/tháng** của đội ngũ điều phối viên, giảm 15% tỷ lệ hủy cuốc do hết pin, tối ưu hóa công suất khai thác đội xe Xanh SM.
3. **Lộ trình triển khai:** 
   - *Tuần 1–2:* Tích hợp Prompt Prototype vào ứng dụng Dispatcher Dashboard nội bộ.
   - *Tuần 3–4:* Thử nghiệm Pilot với 20 điều phối viên ca sáng tại khu vực Hà Nội.
   - *Tháng 2:* Đánh giá kết quả và nhân rộng toàn quốc cho Xanh SM.
