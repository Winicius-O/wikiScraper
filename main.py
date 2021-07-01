from WebScraper import WebScraper

link = "https://pt.wikipedia.org/wiki/Autômato"
x = WebScraper(link)

with open('pretty.html', 'w', encoding='UTF-8') as f:
    f.write(x.htmlContent)

# print(x.getTitle())
# print(x.getTopics())
for i in x.getImageDesc():
    print(i+"\n")