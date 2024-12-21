from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_video, name='upload_video'),
    path('search/', views.search_word, name='search_word'),
    path('count/', views.count_word, name='count_word'),
    path('summary/', views.generate_summary, name='generate_summary'),
]
