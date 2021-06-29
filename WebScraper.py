import requests
import re

class WebScraper:
    regexExpressions = {
        "urlRegex": r'\bhttps:\/\/\w+?\.wikipedia\.org\/wiki\/\S+\b',
    }

    def __init__(self, link) -> None:
        if re.match(self.regexExpressions["urlRegex"], link):
            self.url = link
            self.htmlContent = requests.get(link).text

        else: #re.match == None
            raise Exception("[*] URL inválido")