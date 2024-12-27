from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from albums.models import UserAlbumInteraction




def recommend_albums(user):
    user_interactions = UserAlbumInteraction.objects.filter(user=user)
    
    # Obtén los géneros favoritos o álbumes relacionados
    preferred_genres = set()
    for interaction in user_interactions:
        preferred_genres.add(interaction.album_title)  # Cambia esto según tus datos

    # Busca álbumes relacionados en Whoosh
    ix = open_dir("index")  # Reemplaza con tu índice
    recommendations = []
    with ix.searcher() as searcher:
        for genre in preferred_genres:
            qp = QueryParser("genres", ix.schema)
            q = qp.parse(genre)
            results = searcher.search(q, limit=5)  # Limita el número de resultados
            recommendations.extend([
                {
                    'title': result['title'],
                    'artist': result['artist'],
                    'release_date': result['release_date'],
                    'genres': result['genres'],
                }
                for result in results
            ])
    
    return recommendations