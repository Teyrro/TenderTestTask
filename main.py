import asyncio
import json

from celery import group

from services.work_with_pages_service.async_pages_process import get_pages, get_xml_files
from services.work_with_pages_service.tasks import take_links, parse_xml


def save_result(data):
    with open("result.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    ## TODO Some queries return a 404 error, so some tenders may not be found
    pages_html = asyncio.run(get_pages())
    job = group([
        take_links.s(page) for page in pages_html
    ])
    pages_links = job.apply_async().get()

    ## TODO Some queries return a 404 error, so some tenders may not be found
    xml_files = asyncio.run(get_xml_files(pages_links))
    job = group([
        parse_xml.s(link, xml_file) for link, xml_file in xml_files
    ])
    publish_info = job.apply_async().get()

    save_result(publish_info)




if __name__ == '__main__':
    main()