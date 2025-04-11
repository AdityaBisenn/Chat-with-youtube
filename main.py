from fastapi import FastAPI
from pydantic import BaseModel
from utils.youtube import get_transcript_from_url
from utils.rag import ingest_transcript, ask_question
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class YouTubeInput(BaseModel):
    url: str

class QuestionInput(BaseModel):
    video_id: str
    question: str

@app.post("/ingest")
def ingest_video(input: YouTubeInput):
    video_id, transcript = get_transcript_from_url(input.url)
    ingest_transcript(video_id, transcript)
    return {"message": "Transcript ingested", "video_id": video_id}

@app.post("/ask")
def ask(data: QuestionInput):
    answer = ask_question(data.video_id, data.question)
    print(answer)
    return {"answer": answer}
