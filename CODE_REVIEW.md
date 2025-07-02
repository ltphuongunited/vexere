# ✅ CODE REVIEW – Vexere AI Chatbot POC

---

## 1. ✅ Quy ước code style

- **Ngôn ngữ:** Python 3.10+
- **Chuẩn:** PEP8 + chia module rõ ràng
- **Tên file/module:** snake_case (vd: `after_service.py`)
- **Biến & hàm:** mô tả rõ vai trò (`extract_ticket_code`, `handle_after_service`)
- **Comment:** docstring ngắn + chú thích bước logic chính

---

## 2. ✅ Kiểm thử & CI

### 🧪 Kiểm thử
- Manual qua `gradio_app.py` theo luồng test case mẫu
- Logic xử lý phân intent và multi-turn (`L-2`) được test từng bước
- Debug hỗ trợ qua `print(...)` khi cần

### 🛠️ CI
- Chưa tích hợp CI/CD pipeline
- Có thể bổ sung:
  - `black` + `isort` để lint tự động
  - `pytest` để kiểm thử unit
  - `pre-commit` hook kiểm định trước khi commit

---

## 3. ⚠️ Hạn chế & mở rộng

### ⚠️ Hạn chế
- Chỉ hỗ trợ 1 session giả lập (demo 1 người)
- Chưa xử lý thực tế voice/image (mới placeholder)
- Chưa kết nối DB thật hoặc API booking thực sự
- Classify intent hoàn toàn dựa vào Gemini (chưa có fallback)

### 🌱 Mở rộng
- ✅ Tích hợp PhoWhisper (voice) + BLIP/OCR (image)
- ✅ Session đa người (session_id hoặc Redis)
- ✅ Kết nối data vé/xuất hóa đơn thực
- ✅ Huấn luyện thêm intent classifier domain-specific
- ✅ Dockerize + deploy test
