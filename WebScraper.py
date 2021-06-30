import requests
import re

class WebScraper:
    regexExp = {
        "urlRegex": r'\bhttps:\/\/\w+?\.wikipedia\.org\/wiki\/\S+\b',
        "titleRegex": r'<\s*h1 id="firstHeading" class="firstHeading"\s*>\n*\t*(\w+)'
    }

    def __init__(self, link) -> None:
        if re.match(self.regexExp["urlRegex"], link):
            self.url = link
            self.htmlContent = requests.get(link).text
        else: #re.match == None
            raise Exception("[*] URL inválido")

    def getTitle(self) -> str:
        # retorna o grupo de captura contido no match
        return re.findall(self.regexExp["titleRegex"], self.htmlContent)[0]