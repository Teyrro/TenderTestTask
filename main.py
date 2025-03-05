import asyncio
from concurrent.futures import ThreadPoolExecutor

import requests
from celery import group

from services.work_with_pages_service.async_pages_process import get_pages, get_xml_files
from services.work_with_pages_service.tasks import take_links, parse_xml


def save_result(data):
    with open("result.txt", "w") as file:
        for tup in data:
            file.write(str(tup) + "\n")

def main():
    pages_html = asyncio.run(get_pages())
    job = group([
        take_links.s(page) for page in pages_html
    ])
    pages_links = job.apply_async().get()

    xml_files = asyncio.run(get_xml_files(pages_links))
    job = group([
        parse_xml.s(link, xml_file) for link, xml_file in xml_files
    ])
    publish_info = job.apply_async().get()

    save_result(publish_info)




if __name__ == '__main__':
    main()