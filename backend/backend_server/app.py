from pprint import pprint
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

@app.post("/get_only_titles")
def get_only_titles(request: ExtractTextRequest) -> list[str]:
    return [
    "David Copperfield",
    "The Razor's Edge",
    "The Fountainhead",
    "Jane Eyre",
    "Of Human Bondage"
    ]
    # book_titles = list(set(extract_book_titles(request.text)))

    # if book_titles == ["None"]:
    #     return []
    # return book_titles

class BookDetailsRequest(BaseModel):
    book_title: str
    zipcode: str | None = None

@app.post("/book_details")
async def book_details(request: BookDetailsRequest) -> list[BookFromWorldCat]:
    return await get_a_book(request.book_title, request.zipcode)

@app.post("/extract_titles")
async def extract_text(request: ExtractTextRequest) -> dict[str, list[BookFromWorldCat]]:
    book_titles = list(set(extract_book_titles(request.text)))

    print("extracted book titles:")
    pprint(book_titles)

    if book_titles == ["None"]:
        return {}
    else:
        coro_results = await asyncio.gather(*[get_a_book(title, request.zipcode) for title in book_titles])

        return {
            title: coro_result for title, coro_result in zip(book_titles, coro_results)
        }




