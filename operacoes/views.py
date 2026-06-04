from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpResponse

from acervo.models import Livro
from operacoes.models import Emprestimo
from usuarios.models import Usuario

def painel_emprestimos(request):
    """View para exibir o painel de empréstimos ativos."""
    emprestimos_ativos = Emprestimo.objects.filter(status='ATIVO').order_by('-data_emprestimo')
    return render(request, 'operacoes/painel_emprestimos.html', {
        'emprestimos': emprestimos_ativos
    })

def buscar_emprestimos(request):
    """View consumida pelo HTMX para busca em tempo real."""
    query = request.GET.get('q', '')
    emprestimos = Emprestimo.objects.filter(status='ATIVO')
    
    if query:
        emprestimos = emprestimos.filter(usuario__nome__icontains=query) | \
                      emprestimos.filter(livro__titulo__icontains=query)
                      
    return render(request, 'operacoes/partials/grid_emprestimos.html', {'emprestimos': emprestimos.order_by('-data_emprestimo')})

def realizar_emprestimo(request):
    """View para realizar um empréstimo de livro."""
    livros_disponiveis = Livro.objects.filter(disponivel=True, ativo=True).order_by('titulo')
    usuarios_ativos = Usuario.objects.filter(ativo=True).order_by('nome')
    
    contexto = {
        'livros': livros_disponiveis,
        'usuarios': usuarios_ativos
    }
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        livro_id = request.POST.get('livro_id')
        
        usuario = get_object_or_404(Usuario, id=usuario_id)
        livro = get_object_or_404(Livro, id=livro_id)
        
        try:
            emprestimo = Emprestimo(usuario=usuario, livro=livro)
            emprestimo.save()
            return redirect('operacoes:painel_emprestimos')
        except ValidationError as e:
            # Pega a mensagem de erro da validação do modelo e manda para a tela
            contexto['erro'] = e.messages[0] if hasattr(e, 'messages') else str(e)
            return render(request, 'operacoes/partials/realizar_emprestimo.html', contexto)
        except Exception as e:
            contexto['erro'] = "Ocorreu um erro inesperado."
            return render(request, 'operacoes/partials/realizar_emprestimo.html', contexto)
    
    return render(request, 'operacoes/partials/realizar_emprestimo.html', contexto)

def realizar_devolucao(request, emprestimo_id):
    """View para registrar a devolução (Modal via HTMX)."""
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)
    
    if request.method == 'POST':
        emprestimo.registrar_devolucao()
        return HttpResponse("""
            <script>
                window.location.reload();
            </script>
        """)
    
    return render(request, 'operacoes/partials/realizar_devolucao.html', {'emprestimo': emprestimo})