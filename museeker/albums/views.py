from django.shortcuts import render
from albums import services
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        messages.info(request, "Loading data...")
        services.get_albums()
        messages.success(request, "Data loaded successfully! You can now explore the application.")
    except Exception as e:
        print(f"Error al cargar los álbumes: {e}")
    
    return render(request, 'index.html', {'loaded': loaded})