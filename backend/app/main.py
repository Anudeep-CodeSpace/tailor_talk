import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import QueryRequest, QueryResponse
from .agent_logic import process_query_concurrently
from .utils import encode_image_to_base64

app = FastAPI(title="TailorTalk Titanic Agent")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, 
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/health")
def root():
    return {
        "status": "ok"
    }

@app.post("/chat", response_model=QueryResponse)
async def chat_endpoint(request: QueryRequest):
    try:
        # Offload the blocking LangChain execution to a worker thread
        answer_text, unique_plot_path = await asyncio.to_thread(
            process_query_concurrently, request.query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    image_data = None
    # Check for the uniquely generated file
    if unique_plot_path and os.path.exists(unique_plot_path):
        image_data = encode_image_to_base64(unique_plot_path)

    return QueryResponse(answer=answer_text, image=image_data)