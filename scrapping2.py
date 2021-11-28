import os
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_noticias(url_list):
    url_noticias = []
    print('list: ', url_list)
    req = Request(url_list, headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req).read()
    html = BeautifulSoup(f, 'lxml')
    noticias = html.find_all('div')

    for noticia in noticias:
        url = noticia.find('a')
        sturl = str(url)
        print('url: ', sturl)
        if 'href="https://okdiario.com/espana/' in sturl and not 'ultimas-noticias' in sturl:
            index1 = sturl.index('href="https:/')
            index2 = sturl.index('\"', index1+13)
            url_noticias.append(sturl[index1+13:index2-1])
            print('cut url: ', sturl)
    return url_noticias

def count_words(texto):
    words = texto.split()
    return len(words)

def get_texto_noticias(url, palabras_documento):

    texto = ''
    print('requested url: ', url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req).read()
    noticia = BeautifulSoup(f, 'lxml')
    div = noticia.find('div', id='contentid-0')
    if div is not None:
        parrafos = div.find_all('p')[:-1]

        for parrafo in parrafos:

            if not parrafo.find_all('span'):
                texto += parrafo.text+'\n'

            if count_words(texto) > palabras_documento:
                break

        return texto

    else:
        return None


def escribe_notica(texto, path):
    position = len(os.listdir(path))
    file_name = f'{path}/{position}.txt'
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(texto)


def main(url_base, url_categoria, init_page, folder_path, documentos_totales, palabras_documento):

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    while len(os.listdir(folder_path)) < documentos_totales:
        url_list = f'{url_categoria}/'
        url_noticias = get_noticias(url_list)
        init_page -= 1
        for url in url_noticias:
            if len(os.listdir(folder_path)) > documentos_totales:
                break
            else:
                print('final url: ', f'{url_base}{url}')
                texto = get_texto_noticias(f'{url_base}{url}', palabras_documento)
                if texto:
                    escribe_notica(texto, folder_path)

if __name__ == '__main__':
    url_base = f'https:/'
    documentos_totales = 50
    palabras_documento = 300

    temas = [
        #('okdiario.com/deportes', 'deportes', 1788),
        ('okdiario.com/espana', 'politica', 1489)#,
        #('okdiario.com/salud', 'salud', 140)
        ]

    for categoria, folder_name, init_page in temas:
        url_categoria = f'{url_base}/{categoria}'
        folder_path  = f'./noticias2/{folder_name}'
        main(url_base, url_categoria, init_page, folder_path, documentos_totales, palabras_documento)
