

import asyncio
from pprint import pprint
from typing import List
from pydantic import BaseModel
from urllib.parse import quote_plus
from playwright.async_api import async_playwright, Page, ElementHandle
import functools

class BookFromWorldCat(BaseModel):
    distance_num_miles: float
    distance_str: str
    library_name: str
    book_title: str
    book_author: str

@functools.wraps
def cache_decorator(func):
    cache = {}
    async def wrapped(book_title: str, zip_code: str | None = None):
        if book_title not in cache:
            result = await func(book_title, zip_code)
            cache[book_title] = result
        return cache[book_title]

    return wrapped

@cache_decorator
async def get_a_book(book_title: str, zip_code: str | None) -> list[BookFromWorldCat]:
    url_encoded_book_title = quote_plus(book_title)

    async with async_playwright() as p:
        for browser_type in [p.chromium]:
            browser = await browser_type.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(f'https://worldcat.org/search?q={url_encoded_book_title}')
            await asyncio.sleep(1)
            if btn := await page.query_selector("#onetrust-accept-btn-handler"):
                await btn.click()
                await asyncio.sleep(1)
            list = await page.query_selector("main > div > div > ol")
            links = await list.query_selector_all("li > div > div > div > div > div > h2 > div > a")
            pages: List[Page] = []
            for h in links:
                # Get page after a specific action (e.g. clicking a link)
                async with context.expect_page() as new_page_info:
                    await h.click(modifiers=["Control"])
                pages.append(await new_page_info.value)

            await page.close()
            

            libraries = []
            for page in pages:
                title = await page.query_selector("#__next > div > div > main > div > div > div > div > h1 > div > span")
                book_title: str = await title.inner_text()

                author = await page.query_selector("#__next > div > div > main > div > div > div > div > span > span")
                book_author: str = await author.inner_text()

                list = await page.query_selector("#__next > div > div > main > div > div > div:nth-child(2) > div > div > ul")
                libraries_info = await list.query_selector_all("li > div > div > div")
                for library in libraries_info:
                    title: ElementHandle = await library.query_selector("a > p > strong")
                    distance: ElementHandle = await library.query_selector("div > div > p > strong")

                    library_name: str = await title.inner_text()
                    distance: str = await distance.inner_text()
                    distance_num_miles = float(distance.removesuffix(" miles").replace(",", "").strip())



                    libraries.append(BookFromWorldCat(
                        distance_num_miles=distance_num_miles,
                        distance_str = distance,
                        library_name = library_name,
                        book_title = book_title,
                        book_author = book_author
                    ))
                await page.close()
            
    libraries.sort(key=lambda x: x.distance_num_miles)
    return libraries
