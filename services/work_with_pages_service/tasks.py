import xmltodict
from bs4 import BeautifulSoup

from config.config import settings
from services.my_celery import app



class TakeLinksFromPageTask(app.Task):
    def parse_html(self, source: str):
        soup = BeautifulSoup(source, "html.parser")
        divs = soup.find_all("div", {"class": settings.page.div_class})
        host = settings.target_site.host
        return [host + div.find_all("a")[1].get("href") for div in divs]

    def run(self, page: str) -> list[str]:
        links = self.parse_html(page)
        for i in range(len(links)):
            links[i] = links[i].replace("view", "viewXml")
        return links

class ParseXMLFileTask(app.Task):
    def run(self, link: str, xml_file: str) -> tuple:
        common_info = settings.xml_tags.common
        publish = settings.xml_tags.publish
        xml = next(iter(xmltodict.parse(xml_file).values()))
        result = xml[common_info][publish]
        return link, result


take_links = app.register_task(TakeLinksFromPageTask())
parse_xml = app.register_task(ParseXMLFileTask())