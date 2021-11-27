import os
import urllib.request
from bs4 import BeautifulSoup

def get_noticias(url_list):
    url_noticias = []
    f = urllib.request.urlopen(url_list)
    html = BeautifulSoup(f, 'lxml')
    noticias = html.find_all('div', class_='news-container')

    for noticia in noticias:
        url = noticia.find('a')
        if not ('resumen y goles' in url['title'] or 'Las mejores imágenes del' in url['title']):
            url_noticias.append(url['href'])

    return url_noticias

def count_words(texto):
    words = texto.split()
    return len(words)

def get_texto_noticias(url, palabras_documento):
    
    texto = ''
    f = urllib.request.urlopen(url)
    noticia = BeautifulSoup(f, 'lxml')
    div = noticia.find('div', id='article-body-content')
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
    with open(file_name, 'w') as f:
        f.write(texto)
    

def main(url_base, url_categoria, init_page, folder_path, documentos_totales, palabras_documento):
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    while len(os.listdir(folder_path)) < documentos_totales:
        url_list = f'{url_categoria}/{init_page}/'
        url_noticias = get_noticias(url_list)
        init_page -= 1
        for url in url_noticias:
            if len(os.listdir(folder_path)) > documentos_totales:
                break
            else:
                texto = get_texto_noticias(f'{url_base}{url}', palabras_documento)
                if texto:
                    escribe_notica(texto, folder_path)

if __name__ == '__main__':
    url_base = f'https://www.elespanol.com'
    documentos_totales = 50
    palabras_documento = 300
    
    temas = [
        ('deportes', 'deportes', 1788),
        ('espana', 'politica', 1489),
        ('ciencia/salud', 'salud', 140)]
    
    for categoria, folder_name, init_page in temas:
        url_categoria = f'{url_base}/{categoria}'
        folder_path  = f'./noticias/{folder_name}'
        main(url_base, url_categoria, init_page, folder_path, documentos_totales, palabras_documento)