from django.urls import path
from operacoes import views

app_name = 'operacoes'

urlpatterns = [
    path('', views.painel_emprestimos, name='painel_emprestimos'),
    path('buscar/', views.buscar_emprestimos, name='buscar_emprestimos'),
    path('realizar/', views.realizar_emprestimo, name='realizar_emprestimo'),
    path('devolucao/<int:emprestimo_id>/', views.realizar_devolucao, name='realizar_devolucao'),
]