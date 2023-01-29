from fastapi import FastAPI
from pydantic import BaseModel
from .title_extraction import extract_book_titles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return "Hello World!"

class ExtractTextRequest(BaseModel):http://localhost.tiangolo.com

