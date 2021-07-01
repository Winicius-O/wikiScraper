from WebScraper import WebScraper

link = "https://pt.wikipedia.org/wiki/jornalismo"
x = WebScraper(link)

# with open('pretty.html', 'w', encoding='UTF-8') as f:
#     f.write(x.htmlContent)

print(x.getTitle())
print(x.getTopics())
