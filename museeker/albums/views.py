from django.shortcuts import render, redirect
from albums import services, recommends
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from albums.models import UserAlbumInteraction

@login_required
def album_list(request):
    albums = services.list_albums()
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
        messages.success(request, "Data loaded successfully! You can now explore the application.")
    except Exception as e:
        print(f"Error al cargar los álbumes: {e}")
    
    return render(request, 'index.html', {'loaded': loaded})

@login_required
def user_recommendations(request):
    recommendations = recommends.recommend_albums(request.user)
    return render(request, "recommendations.html", {"recommendations": recommendations})

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