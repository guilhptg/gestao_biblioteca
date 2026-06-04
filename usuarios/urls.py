from django.urls import path
from usuarios import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.painel_usuarios, name='painel_usuarios'),
    path('adicionar/', views.adicionar_usuario, name='adicionar_usuario'),
    path('buscar/', views.buscar_usuarios, name='buscar_usuarios'), 
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'), 
]