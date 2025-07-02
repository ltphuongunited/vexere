from app.rag_faq import answer_faq

if __name__ == "__main__":
    question = "Tôi mang hành lí được không"
    response = answer_faq(question)
    print(response)

# import requests

# def test_chat(user_input: str):
#     url = "http://localhost:8000/chat"
#     payload = {
#         "text": user_input
#     }

#     response = requests.post(url, json=payload)
#     if response.status_code == 200:
#         result = response.json()
#         print("🤖 INTENT:", result.get("intent"))
#         print("💬 REPLY:", result.get("reply"))
#     else:
#         print("❌ Error:", response.status_code, response.text)

# if __name__ == "__main__":
#     # Thử các case:
#     test_chat("Được mang hành lí như thế nào")
#     test_chat("Tôi muốn đổi giờ vé đã đặt hôm qua")
#     test_chat("Mình cần đặt vé xe đi Hà Nội tối nay")
