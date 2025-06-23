import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"
from fastapi import FastAPI
from app.api.endpoints import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Document Entity Extraction API",
    description="OCR, document classification, and entity extraction API.",
    version="1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
