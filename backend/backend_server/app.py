from fastapi import FastAPI
from pydantic import BaseModel

import asyncio
from .book_lookup import BookFromWorldCat, get_a_book
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

class ExtractTextRequest(BaseModel):
    text: str
    zipcode: str | None = None

@app.post("/extract_titles")
async def extract_text(request: ExtractTextRequest) -> dict[str, list[BookFromWorldCat]]:
    book_titles = list(set(extract_book_titles(request.text)))

    if book_titles == ["None"]:
        return {}
    else:
        coro_results = await asyncio.gather(*[get_a_book(title, request.zipcode) for title in book_titles])

        return {
            title: coro_result for title, coro_result in zip(book_titles, coro_results)
        }

        
        

