from django.shortcuts import render
from acervo.models import Livro

def catalogo_publico(request):
    """Renderiza a página principal com todos os livros."""
    livros = Livro.objects.all().order_by('titulo')
    return render(request, 'acervo/index.html', {'livros': livros})

def buscar_livros(request):
    """View de serviço consumida pelo HTMX para busca em tempo real."""
    termo = request.GET.get('q', '')
    if termo:
        # Busca por título ou autor ignorando maiúsculas/minúsculas (icontains)
        livros = Livro.objects.filter(titulo__icontains=termo) | Livro.objects.filter(autor__icontains=termo)
    else:
        livros = Livro.objects.all().order_by('titulo')
        
    return render(request, 'acervo/partials/grid_livros.html', {'livros': livros})