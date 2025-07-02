import os
import json
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_KEY")

# File to store FAISS index (embedding)
INDEX_FILE = "app/sample_data/faq.index"

def build_or_load_faq_vectorstore() -> FAISS:
    """
    Create or load FAISS vectorstore from file.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    if os.path.exists(INDEX_FILE):
        # If index already exists, load it with deserialization allowed
        return FAISS.load_local(
            INDEX_FILE,
            embeddings,
            allow_dangerous_deserialization=True
        )
    
    # If not, load JSON and create embeddings
    try:
        with open("app/sample_data/faq.json", "r", encoding="utf-8") as f:
            faq_data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load FAQ data: {str(e)}")

    docs = [
        Document(
            page_content=f"Q: {item['question']}\nA: {item['answer']}",
            metadata={"question": item["question"]}
        )
        for item in faq_data
    ]

    db = FAISS.from_documents(docs, embeddings)
    db.save_local(INDEX_FILE)
    return db



def answer_faq(query: str) -> str:
    """
    Trả lời câu hỏi FAQ bằng Gemini và FAISS.
    """
    try:
        db = build_or_load_faq_vectorstore()
        retriever = db.as_retriever(search_kwargs={"k": 20})

        llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.0-flash",
            temperature=1,
            convert_system_message_to_human=True
        )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

        result = qa.invoke({"query": query})
        answer = result["result"]

        # Nếu muốn kèm câu trả lời gốc tham chiếu:
        sources = "\n\n".join(doc.page_content for doc in result["source_documents"])
        # return f"💡 **Trả lời:**\n{answer}\n\n📄 **Tham khảo:**\n{sources}"
        print(sources)
        return answer

    except Exception as e:
        return f"❌ Lỗi khi truy vấn FAQ: {str(e)}"
