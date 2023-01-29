

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        for browser_type in [p.chromium]:
            browser = await browser_type.launch(headless=False)
            page = await browser.new_page()
            await page.goto('http://whatsmyuseragent.org/')
            await asyncio.sleep(100)
            await page.screenshot(path=f'example-{browser_type.name}.png')
            await browser.close()

asyncio.run(main())