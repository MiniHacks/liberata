from pprint import pprint
from fastapi import FastAPI
from functools import cache
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

    class Config:
        frozen = True

get_title_hash = {}

@app.post("/get_only_titles")
async def get_only_titles(request: ExtractTextRequest) -> list[str]:
    if request not in get_title_hash:
        book_titles = list(set(await extract_book_titles(request.text)))

        if book_titles == ["None"]:
            result = []
        else:
            result = book_titles
    
        print("adding to cache")
        pprint(request)
        get_title_hash[request] = result

    else:
        print("Cached!!!")

    ret = get_title_hash[request]
    asyncio.gather(*[
        get_or_insert_cache_book_details(BookDetailsRequest(book_title=title, zipcode=request.zipcode))
        for title in ret
    ])

    return ret

class BookDetailsRequest(BaseModel):
    book_title: str
    zipcode: str | None = None


    class Config:
        frozen = True

    

get_book_details_cache = {}

async def get_or_insert_cache_book_details(request: BookDetailsRequest) -> list[BookFromWorldCat]:
    if request not in get_book_details_cache:
        print("oops we have to fetch the following title: " , request.book_title)
        get_book_details_cache[request] = await get_a_book(request.book_title, request.zipcode)
        print("finished fetching the following ttile: " , request.book_title)
    else:
        print("cached the title!!!!!", request.book_title)
    
    return get_book_details_cache[request]


@app.post("/book_details")
async def book_details(request: BookDetailsRequest) -> list[BookFromWorldCat]:
    return await get_or_insert_cache_book_details(request)
    

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




