import asyncio
import logging
from asyncio import create_task, Semaphore
from urllib.parse import urljoin

import aiohttp

from config.config import settings

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s)'
)
logger = logging.getLogger(__name__)

headers = {
    "User-Agent": settings.target_site.headers.UserAgent,
    "Accept": settings.target_site.headers.Accept,
    "Accept-Language": settings.target_site.headers.AcceptLanguage,
    "Accept-Encoding": settings.target_site.headers.AcceptEncoding,
    "Connection": settings.target_site.headers.Connection,
    "Referer": settings.target_site.headers.Referer,
}

async def get_page(
        session: aiohttp.ClientSession,
        url: str,
        number: int,
        timeout: int = 10
) -> str | None:

    try:
        params = settings.target_site.params
        params['pageNumber'] = number

        async with session.get(
                url,
                params=params,
                timeout=aiohttp.ClientTimeout(total=timeout),
        ) as response:
            if response.ok:
                return await response.text()
            logger.warning(f"Page {number} request failed with status {response.status}.")
    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        logger.error(f"Page {number} request error: {str(e)}")

async def get_pages() -> list:
    """Получение всех страниц"""
    page_count = settings.target_site.page_count + 1
    page_link = settings.target_site.page_link
    host = settings.target_site.host
    url = urljoin(host, page_link)

    async with aiohttp.ClientSession(headers=headers) as session:

        pages_requests = [
            create_task(get_page(session, url, i))
            for i in range(1, page_count)
        ]
        responses = await asyncio.gather(*pages_requests)

    return [page for page in responses if page is not None]

async def get_xml_file(
        session: aiohttp.ClientSession,
        url: str,
        s: Semaphore,
        timeout: int = 10
) -> tuple | None:
    async with s:
        try:

            async with session.get(
                    url=url,
                    timeout=aiohttp.ClientTimeout(total=timeout),
            ) as response:
                s.release()
                if response.ok:
                    return url, await response.text()
                logger.warning(f"Xml {url} request failed: HTTP {response.status}.")
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            s.release()
            logger.error(f"Xml {url} request error: {str(e)}.")


async def get_xml_files(pages_links) -> list[str]:
    s = Semaphore(5)
    async with aiohttp.ClientSession(headers=headers) as session:
        all_links = [link for sublist in pages_links for link in sublist]
        tasks = [
            create_task(get_xml_file(session, url, s))
            for url in all_links
        ]
        response = await asyncio.gather(*tasks)
    return [xml for xml in response if xml is not None]