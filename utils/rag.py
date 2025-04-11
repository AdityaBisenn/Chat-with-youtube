import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

load_dotenv()

# Gemini config
llm = GoogleGenerativeAI(model="models/gemini-2.0-flash-lite", google_api_key=os.getenv("GEMINI_API_KEY"))
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GEMINI_API_KEY"))

persist_directory = "chroma_db"
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def ingest_transcript(video_id: str, transcript: str):
    docs = text_splitter.create_documents([transcript], metadatas=[{"video_id": video_id}])
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)
    vectordb.add_documents(docs)
    vectordb.persist()

def ask_question(video_id: str, question: str):
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)
    retriever = vectordb.as_retriever(search_kwargs={"k": 5, "filter": {"video_id": video_id}})
    docs = retriever.get_relevant_documents(question)

    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""Answer the question using only the transcript below (give a detailed answer with complete explaination):

Transcript:
{context}

Question: {question}
"""

    return llm.invoke(prompt).strip()
