from django.shortcuts import render, redirect
from albums import services, recommends
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from albums.models import UserAlbumInteraction

@login_required
def album_list(request):
    albums = services.list_albums()
    print(albums)
    return render(request, 'album_list.html', {'albums': albums})

@login_required
def search_view(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = services.search_albums(str(query))

    results = results if results else []
    return render(request, 'search.html', {'results': results, 'query': query})

@login_required
def filter_by_genre(request):
    selected_genre = request.GET.get('selected_genre', '')
    results = []
    genres = services.get_genres()
    if selected_genre:
        results = services.filter_by_genre(str(selected_genre))

    results = results if results else []
    return render(request, 'filter.html', {'results': results, 'genres': genres, 'selected_genre': selected_genre})

@login_required
def load_data(request):
    loaded = False
    try:
        services.get_albums()
        messages.success(request, "¡Datos cargados con éxito! Ahora puedes explorar la aplicación.")
    except Exception as e:
        print(f"Error al cargar los álbumes: {e}")
    
    return render(request, 'index.html', {'loaded': loaded})

@login_required
def album_detail(request, id):
    interaction, created = UserAlbumInteraction.objects.get_or_create(
        user=request.user,
        album_id=int(id)
    )
    
    album = services.search_albums(str(id), attribute="id")[0]
    
    if request.method == 'POST':
        if 'is_favorite' in request.POST:
            interaction.is_favorite = not interaction.is_favorite
            interaction.save()
            if interaction.is_favorite:
                messages.success(request, "Álbum añadido a favoritos.")
            else:
                messages.info(request, "Álbum eliminado de favoritos.")
        
        elif 'rating' in request.POST:
            try:
                rating = int(request.POST.get('rating'))
                if 1 <= rating <= 5:
                    interaction.rating = rating
                    interaction.save()
                    messages.success(request, "Álbum puntuado correctamente.")
                else:
                    messages.error(request, "La puntuación debe estar entre 1 y 5.")
            except (ValueError, TypeError):
                messages.error(request, "Por favor, introduce un valor válido.")
        
        return redirect('album_detail', id=id)
    
    ratings = [1, 2, 3, 4, 5]
    
    return render(request, 'album_detail.html', {
        'interaction': interaction,
        'ratings': ratings,
        'album':album
    })

@login_required
def user_favorites(request):
    favorites = UserAlbumInteraction.objects.filter(user=request.user, is_favorite=True)
    albums = []
    for favorite in favorites:
        album = services.search_albums(str(favorite.album_id), attribute="id")[0]
        albums.append(album)
    return render(request, "album_favorites.html", {"albums": albums})
from collections import Counter
from collections import Counter

@login_required
def recommend_albums(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    interactions = UserAlbumInteraction.objects.filter(user=user).order_by('-is_favorite')
    favorite_album_ids = set(interaction.album_id for interaction in interactions if interaction.is_favorite)
    genre_count = Counter()

    # Contar los géneros favoritos del usuario
    for interaction in interactions:
        album = services.search_albums(str(interaction.album_id), attribute="id")[0]
        genres = album['genres']
        genre_count.update(genres)

    favorite_genres = [genre for genre, _ in genre_count.most_common(5)]

    # Recolectar álbumes recomendados basados en géneros favoritos
    recommended_album_ids = set()
    recommended_albums = []

    for genre in favorite_genres:
        albums_by_genre = services.filter_by_genre(genre)
        for album in albums_by_genre:
            album_id = int(album['id'])
            if album_id not in favorite_album_ids and album_id not in recommended_album_ids:
                recommended_albums.append(album)
                recommended_album_ids.add(album_id)  # Solo añade el ID al conjunto

    recommended_albums = services.sortRecommends(recommended_albums, favorite_genres)
    return render(request, 'recommendations.html', {
        'albums': recommended_albums,
        'genres': favorite_genres,
    })
