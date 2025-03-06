import asyncio
import aiohttp

from config.config import settings

async def get_page(url: str, number: int) -> str | None:
    params = settings.target_site.params
    params['pageNumber'] = number
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.ok:
                return await response.text()

async def get_pages() -> list:
    page_count = settings.target_site.page_count + 1
    host = settings.target_site.host
    link = host + settings.target_site.page_link

    pages_requests = [asyncio.ensure_future(get_page(link, i)) for i in range(1, page_count)]
    responses = await asyncio.gather(*pages_requests)
    return [page for page in responses if page is not None]

async def get_xml_file(link) -> tuple | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=link) as response:

            if response.ok:
                return link, await response.text()

async def get_xml_files(pages_links) -> list[str]:
    tasks = []
    for page in pages_links:
        for link in page:
            tasks.append(asyncio.ensure_future(get_xml_file(link)))
    response = await asyncio.gather(*tasks)
    return [xml for xml in response if xml is not None]