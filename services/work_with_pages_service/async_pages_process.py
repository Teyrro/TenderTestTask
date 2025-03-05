import asyncio

import aiohttp
import requests
from multidict import MultiDict

from config.config import settings


async def get_page(url: str, number: int) -> str:
    params = settings.target_site.params
    params['pageNumber'] = number
    headers = settings.get_request.html
    params = MultiDict(params)
    # return requests.get(url, headers=headers, params=params).text
    async with aiohttp.ClientSession(headers=headers) as session:
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
    headers = settings.get_request.xml
    # return requests.get(link, headers=headers).text
    async with aiohttp.ClientSession(headers=headers) as session:
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
