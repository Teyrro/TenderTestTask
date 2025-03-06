import asyncio
import concurrent
from concurrent.futures import ThreadPoolExecutor

from celery import group

from services.work_with_pages_service.async_pages_process import get_xml_files, get_pages
from services.work_with_pages_service.tasks import take_links


def save_files(filename: str, exp, data):
    with open(f"test/data/{filename}.{exp}", "w", encoding="utf-8") as file:
        file.write(data)

def load_files(filename: str, exp):
    with open(f"test/data/{filename}.{exp}", "r", encoding="utf-8") as file:
        return file.read()

def upload_test_data():
    pages_html = asyncio.run(get_pages())

    with ThreadPoolExecutor(max_workers=None) as executor:
        tasks = [
            executor.submit(save_files,f"page_{ind}", "html", page )
            for ind, page in enumerate(pages_html)
        ]
    concurrent.futures.wait(tasks)
    job = group([
        take_links.s(page) for page in pages_html
    ])
    pages_links = job.apply_async().get()

    xml_files = asyncio.run(get_xml_files(pages_links))
    with ThreadPoolExecutor(max_workers=None) as executor:
        tasks = [executor.submit(save_files, f"xml_file_{ind}", "xml", xml[1])
                 for ind, xml in enumerate(xml_files)]
    concurrent.futures.wait(tasks)