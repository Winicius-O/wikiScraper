import requests
import re

class WebScraper:
    regexExp = {
        "urlRegex": r'\bhttps:\/\/\w+?\.wikipedia\.org\/wiki\/\S+\b',

        "titleRegexTags": r'<\s*h1 id="firstHeading" class="firstHeading"\s*>\n*\t*',
        "titleRegexContent": r'<\s*h1 id="firstHeading" class="firstHeading"\s*>\n*\t*\w+'
    }

    def __init__(self, link) -> None:
        if re.match(self.regexExp["urlRegex"], link):
            self.url = link
            self.htmlContent = requests.get(link).text
        else: #re.match == None
            raise Exception("[*] URL inválido")

    def getTitle(self) -> str:
        # a informação buscada vem dessa maneira
        # <h1 id="firstHeading" class="firstHeading">
		# 	Jornalismo
		# </h1>
    
        #guarda resultado até o final da formatação html
        tag = re.findall(self.regexExp["titleRegexTags"], self.htmlContent)
        #guarda a formatação html + conteudo da tag
        content = re.findall(self.regexExp["titleRegexContent"], self.htmlContent)
        
        #seu retorno é basicamente a diferença entre as duas regex
        return content[0][len(tag[0]):]