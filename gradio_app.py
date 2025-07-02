import gradio as gr
import requests
from typing import Optional, Tuple, List

API_BASE = "http://localhost:8000"

def call_api_chat(user_text: str) -> Tuple[str, str]:
    """
    Calls the /chat API endpoint with user_text.
    Returns (intent, reply).
    """
    try:
        response = requests.post(f"{API_BASE}/chat", json={"text": user_text})
        if response.status_code == 200:
            data = response.json()
            reply = data.get("reply", "🤖 Không có phản hồi.")
            intent = data.get("intent", "Unknown")
        else:
            reply = f"❌ Lỗi API: {response.status_code}"
            intent = "Error"
    except Exception as e:
        reply = f"⚠️ Lỗi khi gọi API: {str(e)}"
        intent = "Error"
    return intent, reply

def call_api_voice(audio_path: str, user_text: str = "") -> str:
    """
    Calls the /upload-voice API endpoint with audio file.
    Returns reply string.
    """
    try:
        with open(audio_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{API_BASE}/upload-voice", files=files)
            reply = response.json().get("reply", "🤖 Không hiểu nội dung âm thanh.")
    except Exception as e:
        reply = f"⚠️ Lỗi xử lý voice: {str(e)}"
    return reply

def call_api_image(image_path: str, user_text: str = "") -> str:
    """
    Calls the /upload-image API endpoint with image file.
    Returns reply string.
    """
    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{API_BASE}/upload-image", files=files)
            reply = response.json().get("reply", "🤖 Không hiểu nội dung ảnh.")
    except Exception as e:
        reply = f"⚠️ Lỗi xử lý ảnh: {str(e)}"
    return reply

def chatbot_conversation(user_input: str, history: List[List[str]], image: Optional[str], audio: Optional[str]) -> List[List[str]]:
    """
    Handles the Gradio chatbot conversation logic, including multimodal input.
    """
    if image:
        reply = call_api_image(image, user_input or "")
        history.append([f"[🖼 Ảnh] {user_input}", reply])
        return history
    if audio:
        reply = call_api_voice(audio, user_input or "")
        history.append([f"[🎙 Voice] {user_input}", reply])
        return history
    if not user_input or user_input.strip() == "":
        return history + [[user_input, "❗ Vui lòng nhập nội dung."]]
    intent, reply = call_api_chat(user_input)
    tagged_reply = f"[{intent}] {reply}"
    history.append([user_input, tagged_reply])
    return history

def clear_chat() -> Tuple[List, str, None, None]:
    """
    Clears the chat history and input fields.
    """
    return [], "", None, None

# Gradio UI
def build_gradio_ui():
    """
    Builds and launches the Gradio UI for the Vexere chatbot demo.
    """
    with gr.Blocks() as demo:
        gr.Markdown("## 🤖 Vexere Chatbot Demo (Multimodal)")
        chatbot = gr.Chatbot(label="Vexere AI", height=450)
        with gr.Row():
            msg = gr.Textbox(placeholder="Nhập nội dung...", lines=1, label=None, scale=8)
            send_btn = gr.Button("📨 Gửi", scale=1)
            clear_btn = gr.Button("🧹 Xoá", scale=1)
        with gr.Row():
            img_input = gr.Image(type="filepath", label="🖼 Ảnh (tuỳ chọn)", scale=1)
            audio_input = gr.Audio(type="filepath", label="🎙 Voice (tuỳ chọn)", scale=1)
        send_btn.click(
            fn=chatbot_conversation,
            inputs=[msg, chatbot, img_input, audio_input],
            outputs=chatbot
        )
        msg.submit(
            fn=chatbot_conversation,
            inputs=[msg, chatbot, img_input, audio_input],
            outputs=chatbot
        )
        clear_btn.click(fn=clear_chat, outputs=[chatbot, msg, img_input, audio_input])
    return demo

if __name__ == "__main__":
    build_gradio_ui().launch()
