
from django.contrib import admin
from django.urls import path, include
from albums import views

urlpatterns = [
    path('', view=views.album_list, name='album_list'),
    path('search/', view=views.search_view, name='search'),
    path('filter/', view=views.filter_by_genre, name='filter'),
    path('load/', view=views.load_data, name='load_data'),
    path('album/<int:id>/', views.album_detail, name='album_detail'),
    path('favorites/', views.user_favorites, name='favorites'),

]
