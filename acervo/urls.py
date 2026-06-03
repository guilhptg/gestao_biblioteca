from django.urls import path
from acervo import views

app_name = 'acervo'

urlpatterns = [
    path('', views.catalogo_publico, name='catalogo'),
    path('buscar/', views.buscar_livros, name='buscar_livros'), # Endpoint da "API" interna para o HTMX
]