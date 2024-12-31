import os
import urllib.request
from bs4 import BeautifulSoup
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from datetime import datetime
from albums.models import UserAlbumInteraction

from whoosh.fields import Schema, TEXT, ID, DATETIME, KEYWORD
from whoosh.index import create_in

# # Definir el esquema de Whoosh
def create_schema():
    schema = Schema(
        id=ID(stored=True, unique=True),
        title=TEXT(stored=True),
        artist=TEXT(stored=True),
        img=TEXT(stored=True),
        release_date=TEXT(stored=True),
        genres=KEYWORD(stored=True, commas=True)
    )
    return schema


def create_index(schema):
    if not os.path.exists("index"):
        os.mkdir("index")
    return create_in("index", schema)

def get_albums():
    BASE_URL = "https://www.last.fm/music/+releases/out-now/popular?page="
    id = 0
    schema = create_schema()

    ix = create_index(schema)
    UserAlbumInteraction.objects.all().delete()
    for i in range(1, 5):
        response = urllib.request.urlopen(f"{BASE_URL}{i}")
        
        if response.getcode() != 200:
            print(f"HTTPError: {response.getcode()} - Error al acceder a la página.")
            return

        encoding = response.headers.get_content_charset('utf-8')
        soup = BeautifulSoup(response.read().decode(encoding), 'html.parser')

        albums = soup.find_all('li', class_="resource-list--release-list-item-wrap")
        if not albums:
            print("No se encontraron más discos.")
            return
        
        with ix.writer() as writer_index:
            for album in albums:
                title = album.find('h3', class_="resource-list--release-list-item-name").get_text().strip()
                href = album.find('h3', class_="resource-list--release-list-item-name").a['href']
                artist = album.find('p', class_="resource-list--release-list-item-artist").get_text().strip()
                date = album.find('p', class_="resource-list--release-list-item-aux-text resource-list--release-list-item-date").get_text().strip()
                date = datetime.strptime(date, "%d %b %Y").date()
                release_date = date.strftime("%Y-%m-%d")

                # Obtén la URL de la imagen
                with urllib.request.urlopen(f"https://www.last.fm{href}") as response:
                    album_soup = BeautifulSoup(response.read().decode(encoding), 'html.parser')
                    tags = album_soup.find_all('li', class_="tag")
                    genres = set()
                    for tag in tags:
                        if tag.get_text().strip() != '':
                            genres.add(tag.get_text().strip())
                    genres = ",".join(genres)
                    img = album_soup.find('a', class_="cover-art")
                    if img:
                        img = img.img['src']
                    else:
                        img = '/static/images/portada_default.jpg'
                # Indexa la imagen directamente en el documento
                writer_index.add_document(id=str(id), title=title, artist=artist, release_date=release_date, genres=genres, img=img)
                id += 1

    print("Scraping e indexación completados.")


def search_albums(query, attribute="title"):
    ix = open_dir("index")
    with ix.searcher() as searcher:
        qp = QueryParser(attribute, ix.schema)
        q = qp.parse(query)
        results = searcher.search(q, limit=None)
        return [
            {
                'id': result['id'],
                'title': result['title'],
                'artist': result['artist'],
                'release_date': result['release_date'],
                'genres': [genre.strip() for genre in result['genres'].split(",")],
                'img': result.get('img', '../static/img/portada_default.jpg'),
            }
            for result in results
        ]
    
def list_albums():
    try:
        ix = open_dir("index")
        with ix.searcher() as searcher:
            results = list(searcher.documents())
        albums = [
            {
                'id': result['id'],
                'title': result['title'],
                'artist': result['artist'],
                'release_date': result['release_date'],
                'genres': [genre.strip() for genre in result['genres'].split(",")],
                'img': result.get('img', '../static/img/portada_default.jpg'),
            }
            for result in results
        ]
        return albums
    except Exception as e:
        print(f"Error al listar los álbumes: {e}")
        return []


def get_genres():
    try:
        ix = open_dir("index")
        with ix.searcher() as searcher:
            results = searcher.documents()
            genres = set()
            for result in results:
                genres.update([genre.strip() for genre in result['genres'].split(",")])
            return list(genres)
        
    except Exception as e:
        print(f"Error al listar los géneros: {e}")
        return []

def filter_by_genre(genre):
    ix = open_dir("index")
    with ix.searcher() as searcher:
        qp = QueryParser("genres", ix.schema)
        q = qp.parse(f'"{genre}"')
        results = searcher.search(q, limit=None)
        return [
            {
                'id': result['id'],
                'title': result['title'],
                'artist': result['artist'],
                'release_date': result['release_date'],
                'genres': [genre.strip() for genre in result['genres'].split(",")],
                'img': result.get('img', '../static/img/portada_default.jpg'),
            }
            for result in results
        ]

def sortRecommends(recommended_albums, favorite_genres):
    recommended_albums.sort(key=lambda album: len(set(album['genres']).intersection(favorite_genres)), reverse=True)
    return recommended_albums[:10]