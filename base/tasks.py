import asyncio

import nest_asyncio
from celery import shared_task
from playwright.async_api import async_playwright

nest_asyncio.apply()  # for Windows


@shared_task
def run_playwright():
    asyncio.run(main())


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        print(await page.title())
        await browser.close()
