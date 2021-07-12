import bs4
import requests
from bs4 import BeautifulSoup

x = requests.get("https://pt.wikipedia.org/wiki/Semana_de_Arte_Moderna").text

html = BeautifulSoup(x, 'html.parser')

with open('pretty.html', 'w', encoding='UTF-8') as f:
    f.write(html.find_all('ol', {'class': 'references'})[0].prettify())