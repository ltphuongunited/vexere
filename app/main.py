from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from app.rag_faq import answer_faq
from app.after_service import handle_after_service
from app.media_placeholder import process_voice, process_image
from app.utils import classify_intent
from typing import Dict, Any

app = FastAPI()

# Temporary session state for after-service demo (single flow)
session_state: Dict[str, Any] = {"after_service": []}

class UserMessage(BaseModel):
    text: str

@app.post("/chat")
def chat(message: UserMessage) -> Dict[str, str]:
    """
    Main chat endpoint. Classifies intent and routes to appropriate handler.
    """
    text = message.text.strip()
    intent = classify_intent(text)

    if intent == "greeting":
        reply = "👋 Xin chào! Tôi là trợ lý ảo của Vexere. Tôi có thể giúp bạn về đặt vé, đổi giờ vé và thông tin thường gặp."
    elif intent == "L-1":
        reply = answer_faq(text)
    elif intent == "L-2":
        # Use session_state to store after-service flow
        reply, session_state["after_service"] = handle_after_service(
            text,
            session_state["after_service"]
        )
    else:
        reply = "🤖 Xin lỗi, tôi chưa hiểu rõ yêu cầu của bạn. Bạn có thể hỏi về hoàn vé, đổi giờ hoặc đặt vé."

    return {"intent": intent, "reply": reply}

@app.post("/upload-voice")
def upload_voice(file: UploadFile) -> Dict[str, str]:
    """
    Endpoint for processing voice uploads (placeholder).
    """
    return {"reply": process_voice(file)}

@app.post("/upload-image")
def upload_image(file: UploadFile) -> Dict[str, str]:
    """
    Endpoint for processing image uploads (placeholder).
    """
    return {"reply": process_image(file)}