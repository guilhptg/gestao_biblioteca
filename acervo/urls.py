from django.urls import path
from acervo import views

app_name = 'acervo'

urlpatterns = [
    path('', views.catalogo_publico, name='catalogo'),
    path('buscar/', views.buscar_livros, name='buscar_livros'), # Endpoint da "API" interna para o HTMX
    path('adicionar/', views.adicionar_livro, name='adicionar_livro'), # Página para adicionar um novo livro
    path('editar/<int:livro_id>/', views.editar_livro, name='editar_livro'), # Página para editar um livro existente
    path('excluir/<int:livro_id>/', views.excluir_livro, name='excluir_livro'), # Endpoint para exclusão lógica de um livro
]