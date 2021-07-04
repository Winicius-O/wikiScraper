from WebScraper import WebScraper
import os

def menu():
    message = """digite a ação:
[1]Listar tópicos do indice
[2]Listar nomes de arquivos de imagem
[3]Listar referencias bibliográficas
[4]Listar links para outros artigo
[5]Listar todas as informações
[6]Salvar em arquivo...
[0]Sair"""

    print(message)

def listarTopicos(webScraper: WebScraper):
    content = webScraper.getTopics()

    print("\nTópicos do índice:")
    if content == None:
        print("\tNão há tópicos nessa página")
        print("")
        return

    for i in content:
        print("\t"+i)
        
    print("")

def listarDescricoesImg(webScraper: WebScraper):
    content = webScraper.getImageDesc()

    print("\nDescrições das imagens:")
    if content == None:
        print("\tNão há imagens nessa página")
        print("\n")
        return

    for i in content:
        print("\t"+i)
        
    print("")

def listarBibliografia(webScraper: WebScraper):
    print("\nReferências bibliográficas:")
    print("\tEssa função não foi implementada ainda")
    print("")

def listarArtigos(webScraper: WebScraper):
    content = webScraper.getArticles()

    print("\nArtigos:")
    if content == None:
        print("\tNão há links para outros artigos nessa página")
        print("")
        return

    for i in range(len(content)):
        print(f'\t{i}) {content[i][1]} -> {webScraper.url}{content[i][0]}')
        
    print("")

def salvarArquivo(webScraper: WebScraper):
    pass


print("WebScraper")

isValido = False
while not isValido:
    # userInput = input("insira o link da pagina Wikipedia: ")

    try:
        # webScraper = WebScraper(userInput)
        # webScraper = WebScraper('https://pt.wikipedia.org/wiki/brasil')
        webScraper = WebScraper('https://pt.wikipedia.org/wiki/Samba-exalta%C3%A7%C3%A3o')
        isValido = True
    except:
        print("o link inserido é inválido, tente novamente.")


print('Bem vindo!')
menu()

userInput = -1
while userInput != 0:
    userInput = input("insira a ação [M: voltar ao menu | 0: sair do programa]-> ")

    if userInput.upper() == 'M':
        os.system('cls')
        menu()
    elif userInput == '0':
        break
    elif userInput == '1':
        listarTopicos(webScraper)
    elif userInput == '2':
        listarDescricoesImg(webScraper)
    elif userInput == '3':
        listarBibliografia(webScraper)
    elif userInput == '4':
        listarArtigos(webScraper)
    elif userInput == '5':
        listarTopicos(webScraper)
        listarDescricoesImg(webScraper)
        listarBibliografia(webScraper)
        listarArtigos(webScraper)
    elif userInput == '6':
        salvarArquivo(webScraper)
    else:
        print("\n\nopção inválida!")