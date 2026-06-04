from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from usuarios.models import Usuario, Aluno, Professor

def painel_usuarios(request):
    """Renderiza a página principal listando os usuários ativos."""
    usuarios = Usuario.objects.filter(ativo=True).order_by('nome')
    return render(request, 'usuarios/painel_usuarios.html', {'usuarios': usuarios})

def buscar_usuarios(request):
    """View consumida pelo HTMX para busca em tempo real."""
    termo = request.GET.get('q', '')
    usuarios_ativos = Usuario.objects.filter(ativo=True)
    
    if termo:
        usuarios = usuarios_ativos.filter(nome__icontains=termo) | \
                   usuarios_ativos.filter(email__icontains=termo) | \
                   usuarios_ativos.filter(matricula__icontains=termo)
    else:
        usuarios = usuarios_ativos.order_by('nome')
    
    return render(request, 'usuarios/partials/grid_usuarios.html', {'usuarios': usuarios})

def adicionar_usuario(request):
    if request.method == 'POST':
        tipo_usuario = request.POST.get('tipo_usuario')
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        matricula = request.POST.get('matricula')
        ativo = request.POST.get('ativo') == 'on'
        
        if tipo_usuario == 'aluno':
            curso = request.POST.get('curso')
            Aluno.objects.create(nome=nome, cpf=cpf, email=email, matricula=matricula, ativo=ativo, curso=curso)
        elif tipo_usuario == 'professor':
            departamento = request.POST.get('departamento')
            Professor.objects.create(nome=nome, cpf=cpf, email=email, matricula=matricula, ativo=ativo, departamento=departamento)
        
        # Redireciona de volta para o painel após salvar
        return redirect('usuarios:painel_usuarios')
    
    return render(request, 'usuarios/partials/adicionar_usuario.html')

def editar_usuario(request, usuario_id):
    usuario_base = get_object_or_404(Usuario, id=usuario_id)
    
    # Descobre a instância real para mandar pro template
    usuario = getattr(usuario_base, 'aluno', getattr(usuario_base, 'professor', usuario_base))
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        ativo = request.POST.get('ativo') == 'on'
        
        usuario.editar_usuario(nome=nome, email=email, ativo=ativo)
        
        # Edita campos específicos das subclasses se existirem
        if hasattr(usuario, 'alterar_curso') and request.POST.get('curso'):
            usuario.alterar_curso(request.POST.get('curso'))
        elif hasattr(usuario, 'alterar_departamento') and request.POST.get('departamento'):
            usuario.alterar_departamento(request.POST.get('departamento'))
            
        return redirect('usuarios:painel_usuarios')
    
    return render(request, 'usuarios/partials/editar_usuario.html', {'usuario': usuario})

def excluir_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        # Exclusão Lógica
        usuario.excluir_usuario()
        
        # Retorna script para fechar o modal HTMX e atualizar a tela
        return HttpResponse("""
            <script>
                window.location.reload();
            </script>
        """)
        
    return render(request, 'usuarios/partials/modal_excluir.html', {'usuario': usuario})