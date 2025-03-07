import xmltodict
from bs4 import BeautifulSoup
from celery import shared_task

from config.config import settings
from services.my_celery import app



class TakeLinksFromPageTask(app.Task):
    def parse_html(self, source: str):
        soup = BeautifulSoup(source, "html.parser")
        divs = soup.find_all("div", {"class": settings.page.div_class})
        host = settings.target_site.host
        return [host + div.find_all("a")[1].get("href") for div in divs]

    def run(self, page: str) -> list[str]:
        pass

class ParseXMLFileTask(app.Task):
    def run(self, link: str, xml_file: str) -> tuple:
        pass


@shared_task(bind=True, base=TakeLinksFromPageTask)
def take_links(self, page: str):
    links = self.parse_html(page)
    for i in range(len(links)):
        links[i] = links[i].replace("view", "viewXml")
    return links

@shared_task(bind=True, base=ParseXMLFileTask)
def parse_xml(self, link: str, xml_file: str):
    common_info = settings.xml_tags.common
    publish = settings.xml_tags.publish
    xml = next(iter(xmltodict.parse(xml_file).values()))
    result = xml[common_info][publish]
    return link, result
