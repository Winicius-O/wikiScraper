import requests
from bs4 import BeautifulSoup
import re
import json
import os

class WebScraper:
    regexExp = {
        "urlRegex": r'(https:\/\/\w+?\.wikipedia\.org)(\/wiki\/\S+)',
        "tagRemoverRegex": r'<.*>',
        "separaLinkRegex": r'<.*\shref="(.*)"\s.*>',
        "titleRegex": r'<h1 class="firstHeading" id="firstHeading">[\n\s]*(.+)[\n\s]*</h1>',
        "topicsRegex": r'<span class="toctext">[\n\s]*(.+)[\n\s]*<\/span>',
        "imgDescRegex": r'<div class="thumbcaption">\s*<div class="magnify">\s*<a.*>\s*<\/a>\s*<\/div>(?:(?!<\/div>)[\s\S])*',
        "imgLinkRegex": r'<div.*class="thumbinner".*>\s*<a class="image" href="(/wiki/.+\..+)">',
        "bioRegex": r'<span\sclass="reference-text">\s*<cite.*>(?:(?!<\/cite>)[\s\S])*',
        "articlesRegex": r'<a .*href="(\/wiki\/.*)".*title="(.*)".*>[\n\s]*.*[\n\s]*<\/a>'
    }


    def __init__(self, link) -> None:
        if re.match(self.regexExp["urlRegex"], link):

            #guardando url como uma lista de 2 elementos [endereço, rota]
            self.url = re.findall(self.regexExp['urlRegex'], link)[0]

            requestsContent = requests.get(link).text
            #objeto beautifulsoup, utilizado para métodos em que é importante limitar um escopo
            #do html
            self.soup = BeautifulSoup(requestsContent, 'html.parser')
            #conteudo html da pagina
            self.htmlContent = self.soup.prettify()
        
        #tratamento de erro
        else: #re.match == None
            raise Exception("[*] URL inválido")


    def getTitle(self) -> str:
        # retorna o grupo de captura contido no match
        try:
            return re.findall(self.regexExp["titleRegex"], self.htmlContent)[0]
        except:
            return None


    def getTopics(self) -> list:
        content = re.findall(self.regexExp["topicsRegex"], self.htmlContent)

        if len(content)!=0:
            return content
        else:
            return None


    def getImage(self) -> list:
        content = re.findall(self.regexExp["imgDescRegex"], self.htmlContent)
        imgLinks = re.findall(self.regexExp["imgLinkRegex"], self.htmlContent)

        #tratamento dos elementos encontrados
        temp = []
        listaFormatacao = []
        for i in range(len(content)):
            listaFormatacao = []
            #removendo tags html dos elementos achados
            filtragem = re.sub(self.regexExp["tagRemoverRegex"], "", content[i])
            #limpando identação restante
            filtragem = re.sub("\n\s*", " ", filtragem)
            listaFormatacao.append(filtragem)
            listaFormatacao.append(imgLinks[i])
            temp.append(listaFormatacao.copy())


        if len(content)!=0:
            return temp
        else:
            return None


    def getBio(self) -> list:
        #isolando todas as tags span de classe desejada
        newBody = self.soup.find_all('span', {'class': 'reference-text'})
        if len(newBody) == 0:
            return None
        
        # content = re.findall(self.regexExp["bioRegex"], newBody)

        # é criado duas listas para fazer a formatação armazenada, o objetivo é conseguir
        # uma lista com este exemplo de formato:
        # [[conteudoTag1, [link1, link2]], [conteudoTag2, [link1]], ...]
        temp = []
        formataLista = []
        for i in newBody:
            formataLista = []

            # para cada referencia, é verificado a existencia de links, os links são separados
            # usando regex 
            links = i.find_all('a', {'class': 'external text'})
            def separaLinks(x) -> str:
                try:
                    return re.findall(self.regexExp["separaLinkRegex"], str(x))[0]
                except:
                    return None

            links = list(map(lambda x: separaLinks(x), links))

            #FILTRAGEM DO CONTEUDO DA TAG:
            #removendo tags html dos elementos achados
            filtragem = re.sub(self.regexExp["tagRemoverRegex"], "", i.prettify())
            #limpando identação restante
            filtragem = re.sub("\n\s*", " ", filtragem)
            
            formataLista.append(filtragem)
            formataLista.append(links)
            temp.append(formataLista.copy())

        if len(temp)!=0:
            return temp
        else:
            return None


    def getArticles(self) -> list:
        #isolando o html para o escopo do conteudo importante da página, a filtragem é capaz
        #de funcionar sem a necessidade dessa alteração, mas para deixar o conteudo retornado
        #mais interessante, foi escolhido deixar assim
        newBody = self.soup.find_all('div', {'class': 'mw-parser-output'})
        if len(newBody) != 0:
            newBody = newBody[0].prettify()
        else:
            return None

        content = re.findall(self.regexExp["articlesRegex"], newBody)

        if len(content)!=0:
            return content
        else:
            return None


    def jsonGen(self) -> None:
        temp = {}
        temp["url"] = self.url[0] + self.url[1]
        temp["titulo"] = self.getTitle()
        temp["topicos"] = self.getTopics()
        temp["imagens"] = self.getImage()

        artigos = self.getArticles()
        if artigos != None:
            #adicionando aos links o endereço base antes de adiciona-los ao dicionário
            artigos = list(map(lambda x: [self.url[0]+x[0], x[1]], artigos))

        temp["artigos"] = artigos
        temp["referencias"] = self.getBio()

        #criando uma pasta caso ela não exista
        folderPATH = ".\\arquivosJSON\\"
        if not os.path.exists(folderPATH):
            os.makedirs(folderPATH)

        with open(f'{folderPATH}{self.getTitle()}.json', 'w', encoding='UTF-8') as f:
            json.dump(temp, f, indent=4, ensure_ascii=False)