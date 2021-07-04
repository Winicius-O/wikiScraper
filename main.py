from WebScraper import WebScraper

link = "oi"
x = WebScraper(link)

with open('pretty.html', 'w', encoding='UTF-8') as f:
    f.write(x.htmlContent)

# print(x.getTitle())
# print(x.getTopics())