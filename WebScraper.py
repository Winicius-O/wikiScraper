import requests
from bs4 import BeautifulSoup
import re

class WebScraper:
    regexExp = {
        "urlRegex": r'(https:\/\/\w+?\.wikipedia\.org)\/wiki\/\S+',
        "tagRemoverRegex": r'<.*>',
        "titleRegex": r'<h1 class="firstHeading" id="firstHeading">[\n\s]*(.+)[\n\s]*</h1>',
        "topicsRegex": r'<span class="toctext">[\n\s]*(.+)[\n\s]*<\/span>',
        "imgRegex": r'<div class="thumbcaption">\s*<div class="magnify">\s*<a.*>\s*<\/a>\s*<\/div>(?:(?!<\/div>)[\s\S])*',
        "articlesRegex": r'<a .*href="(\/wiki\/.*)".*title="(.*)".*>[\n\s]*.*[\n\s]*<\/a>'
    }

    def __init__(self, link) -> None:
        if re.match(self.regexExp["urlRegex"], link):
            self.url = re.findall(self.regexExp['urlRegex'], link)[0]
            requestsContent = requests.get(link).text
            self.soup = BeautifulSoup(requestsContent, 'html.parser')
            self.htmlContent = self.soup.prettify()
            
        else: #re.match == None
            raise Exception("[*] URL inválido")

    def getTitle(self) -> str:
        # retorna o grupo de captura contido no match
        return re.findall(self.regexExp["titleRegex"], self.htmlContent)[0]

    def getTopics(self) -> list:
        content = re.findall(self.regexExp["topicsRegex"], self.htmlContent)

        if len(content)!=0:
            return content
        else:
            return None

    def getImageDesc(self) -> list:
        content = re.findall(self.regexExp["imgRegex"], self.htmlContent)

        #tratamento dos elementos encontrados
        temp = []
        for i in content:
            #removendo tags html dos elementos achados
            filtragem = re.sub(self.regexExp["tagRemoverRegex"], "", i)
            #limpando identação restante
            filtragem = re.sub("\n\s*", " ", filtragem)
            temp.append(filtragem)

        if len(content)!=0:
            return temp
        else:
            return None

    def getArticles(self) -> list:
        newBody = self.soup.find_all('div', {'class': 'mw-parser-output'})[0].prettify()
        content = re.findall(self.regexExp["articlesRegex"], newBody)

        if len(content)!=0:
            return content
        else:
            return None