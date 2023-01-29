from fastapi import FastAPI
from pydantic import BaseModel
from .title_extraction import extract_book_titles

app = FastAPI()

@app.get("/")
async def root():
    return "Hello World!"

class ExtractTextRequest(BaseModel):
    text: str

@app.post("/extract_text")
def extract_text(request: ExtractTextRequest) -> list[str]:
    return extract_book_titles(request.text)
