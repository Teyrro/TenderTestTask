from celery import group

from config.config import settings
from services.work_with_pages_service.tasks import take_links, parse_xml

def test_take_links_task(celery_app, celery_worker, load_html):

    pages = load_html
    host = settings.target_site.host
    first_xml_url = "/epz/order/notice/printForm/viewXml.html?regNumber=0338100003725000008"
    tasks = [take_links.s(page)
                 for page in pages
                 ]

    job = group(tasks)
    pages_links = job.apply_async().get()
    assert len(pages_links) == 2
    assert len(pages_links[0]) == len(pages_links[1])
    assert pages_links[0][0] == host + first_xml_url

def test_parse_xml_task(celery_app, celery_worker, load_xml):
    files = load_xml
    first_publish = "2025-02-25T14:52:35.208+12:00"

    job = group([parse_xml.s(None, file)
                 for file in files
                 ])
    pages_links = job.apply_async().get()
    assert len(pages_links) == 20
    assert pages_links[0][1] == first_publish
