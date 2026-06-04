from django.shortcuts import render, redirect
from acervo.models import Livro

def catalogo_publico(request):
    """Renderiza a página principal com todos os livros."""
    livros_ativos = Livro.objects.filter(ativo=True).order_by('titulo')
    return render(request, 'acervo/index.html', {'livros': livros_ativos})

def buscar_livros(request):
    """View de serviço consumida pelo HTMX para busca em tempo real."""
    termo = request.GET.get('q', '')
    
    livros_ativos = Livro.objects.filter(ativo=True)
        
    if termo:
        livros = livros_ativos.filter(titulo__icontains=termo) | livros_ativos.filter(autor__icontains=termo)
    else:
        livros = livros_ativos.order_by('titulo')
        
    return render(request, 'acervo/partials/grid_livros.html', {'livros': livros})

def adicionar_livro(request):
    """View para adicionar um novo livro ao acervo."""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        isbn = request.POST.get('isbn')
        ano_publicacao = request.POST.get('ano_publicacao')
        editora = request.POST.get('editora')
        
        # Criar e salvar o novo livro
        Livro.objects.create(
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            ano_publicacao=ano_publicacao,
            editora=editora
        )
        
        # Redirecionar para a página principal após adicionar o livro
        return redirect('acervo:catalogo')
    
    return render(request, 'acervo/modals/adicionar_livro.html')

def editar_livro(request, livro_id):
    """View para editar um livro existente (a ser implementada)."""
    livro = Livro.objects.get(id=livro_id)
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        isbn = request.POST.get('isbn')
        ano_publicacao = request.POST.get('ano_publicacao')
        editora = request.POST.get('editora')
        
        # Usar o método de encapsulamento para editar o livro
        livro.editar_livro(
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            ano_publicacao=ano_publicacao,
            editora=editora
        )
        
        return redirect('acervo:catalogo')
    return render(request, 'acervo/modals/editar_livro.html', {'livro': livro})

def excluir_livro(request, livro_id):
    livro = Livro.objects.get(id=livro_id)
    if request.method == 'POST':
        livro.excluir_livro()  # Realiza exclusão lógica
        return redirect('acervo:catalogo')
    return render(request, 'acervo/modals/excluir_livro.html', {'livro': livro})