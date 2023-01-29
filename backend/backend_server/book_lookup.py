

import asyncio
from pprint import pprint
from typing import List
from pydantic import BaseModel
from urllib.parse import quote_plus
from playwright.async_api import async_playwright, Page, ElementHandle
import functools

class Library(BaseModel):
    distance_num_miles: float
    distance_str: str
    library_name: str
    link_to_borrow: str | None


class BookFromWorldCat(BaseModel):
    available_at: list[Library]
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


            btn = None
            page = await context.new_page()
            if zip_code is not None:
                await page.goto(f'https://worldcat.org/')

                if btn := await page.wait_for_selector("#onetrust-accept-btn-handler", timeout=1000.0):
                    await btn.click()
                
                loc_selector = await page.query_selector("#__next > header > nav > div > button#location-confirmer-desktop > span > div")
                await loc_selector.click()

                textbox = await page.wait_for_selector("div > div > div > div > div > div > input")
                await textbox.click()
                await textbox.type(zip_code, delay=300)
                await textbox.click()
                await page.wait_for_selector("body > div.MuiAutocomplete-popper")
                await textbox.press('Enter')

                btn = await page.query_selector("body > div > div > div > div > div > button > span > div")
                await btn.click()
                
            try:
                await page.goto(f'https://worldcat.org/search?q={url_encoded_book_title}')
            except TimeoutError:
                print(f"uh oh timed out on {book_title}")
                return []
            if btn is None and (btn := await page.wait_for_selector("#onetrust-accept-btn-handler", timeout=1000.0)):
                await btn.click()
            list = await page.wait_for_selector("main > div > div > ol", timeout = 5000.0)
            if list is None:
                return []
            links = await list.query_selector_all("li > div > div > div > div > div > h2 > div > a")
            pages: List[Page] = []
            for h, _ in zip(links, range(2)):
                # Get page after a specific action (e.g. clicking a link)
                async with context.expect_page() as new_page_info:
                    await h.click(modifiers=["Control"])
                pages.append(await new_page_info.value)

            await page.close()
            
            book: List[BookFromWorldCat] = []
            for page in pages:
                title = await page.wait_for_selector("#__next > div > div > main > div > div > div > div > h1 > div > span")
                book_title: str = await title.inner_text()

                author = await page.query_selector("#__next > div > div > main > div > div > div > div > span > span")
                if author:
                    book_author: str = await author.inner_text()
                else:
                    book_author: str = "author not found ???"

                libraries: List[Library] = []
                list = await page.wait_for_selector("#__next > div > div > main > div > div > div:nth-child(2) > div > div > ul")
                await list.wait_for_selector("li > div > div > div")
                libraries_info = await list.query_selector_all("li > div > div > div")
                for library in libraries_info:
                    title: ElementHandle = await library.query_selector("a > p > strong")
                    distance: ElementHandle = await library.query_selector("div > div > p > strong")
                    link: ElementHandle = await library.query_selector("div > div > a")

                    if link is not None:
                        link_to_borrow: str | None = "https://worldcat.org" + await link.get_attribute("href")
                    else:
                        link_to_borrow = None

                    library_name: str = await title.inner_text()
                    distance: str = await distance.inner_text()
                    distance_num_miles = float(distance.removesuffix(" miles").removesuffix(" mile").replace(",", "").strip())


                    libraries.append(Library(
                        distance_num_miles=distance_num_miles,
                        distance_str= distance,
                        library_name=library_name,
                        link_to_borrow=link_to_borrow
                    ))


                libraries.sort(key=lambda x: x.distance_num_miles)
                book.append(BookFromWorldCat(
                    book_title = book_title,
                    book_author = book_author,
                    available_at=libraries
                ))
                await page.close()
            
    return book
