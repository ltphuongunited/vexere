from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from typing import Optional

# Load environment variables once at module level
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_KEY")

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash",
    temperature=0.0
)

def classify_intent(user_input: str) -> str:
    """
    Classifies user input into one of the following intents:
    - greeting: Greeting the chatbot (hello, chào bạn...)
    - L-1: Frequently asked questions (refund policy, luggage, schedules, etc.)
    - L-2: After-service request (providing ticket info, changing time, etc.)
    Returns: intent as a string (greeting, L-1, L-2)
    """
    prompt = f"""
    You are an intent classifier for a travel assistant.

    Classify user input into one of the following intents:
    - greeting: Greeting the chatbot (hello, chào bạn...).
    - L-1: Frequently asked questions (refund policy, luggage, schedules, how to change time, customer support info).
    - L-2: After-service request: Providing actual ticket info like mã vé, yêu cầu đổi giờ cụ thể.

    Only return one of: greeting, L-1, L-2,

    Input: "{user_input}"
    Intent:
    """
    try:
        result = llm.invoke(prompt)
        return result.content.strip()
    except Exception as e:
        # Log error or handle as needed
        return "error"
