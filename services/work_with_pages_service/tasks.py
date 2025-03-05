import datetime

import xmltodict
from bs4 import BeautifulSoup

from config.config import settings
from services.my_celery import app

def parse_html(source: str):
    soup = BeautifulSoup(source, "html.parser")
    divs = soup.find_all("div", {"class": settings.page.div_class})
    host = settings.target_site.host
    return [host + div.find_all("a")[1].get("href") for div in divs]


@app.task
def take_links(page: str) -> list[str]:
    links = parse_html(page)
    for i in range(len(links)):
        links[i] = links[i].replace("view", "viewXml")
    return links


@app.task()
def parse_xml(link: str, xml_file: str) -> tuple:
    common_info = settings.xml_tags.common
    publish = settings.xml_tags.publish
    xml = next(iter(xmltodict.parse(xml_file).values()))
    result = xml[common_info][publish]
    return link, result

