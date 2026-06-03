from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from usuarios.models import Usuario
from acervo.models import Livro


class Emprestimo(models.Model):
    __table_name__ = 'emprestimos'  # Nome explícito da tabela para clareza e controle
    
    # Relacionamentos que mapeiam o diagrama de classes
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="emprestimos")
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="historico_emprestimos")
    data_emprestimo = models.DateTimeField(default=timezone.now)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=[('ATIVO', 'Ativo'), ('DEVOLVIDO', 'Devolvido')], 
        default='ATIVO'
    )

    def clean(self):
        """
        Validação robusta em nível de modelo (Princípio: Fat Models, Skinny Views).
        Centraliza a regra de negócio para evitar estados inválidos no banco.
        """
        super().clean()
        
        if self.pk is None: # Se for um novo empréstimo
            if not self.livro.disponivel:
                raise ValidationError("Este exemplar não está disponível para empréstimo.")
            
            # Contagem de empréstimos ativos do usuário
            ativos = Emprestimo.objects.filter(usuario=self.usuario, status='ATIVO').count()
            
            # Utiliza a propriedade polimórfica definida em Aluno/Professor
            # Para acessar a subclasse real a partir do Usuario base, usamos o getattr do Django
            usuario_real = getattr(self.usuario, 'aluno', getattr(self.usuario, 'professor', self.usuario))
            
            if ativos >= usuario_real.limite_emprestimo:
                raise ValidationError(f"O usuário atingiu o limite máximo de {usuario_real.limite_emprestimo} empréstimos.")

    def save(self, *args, **kwargs):
        """Sobrescreve o salvamento para atualizar os estados envolvidos"""
        self.full_clean()  # Garante que as validações do clean() sejam executadas
        
        if self.pk is None:
            # Ao criar, torna o livro indisponível
            self.livro.disponivel = False
            self.livro.save()
            
        super().save(*args, **kwargs)

    def registrar_devolucao(self):
        """Método encapsulado para finalizar a operação com segurança"""
        self.status = 'DEVOLVIDO'
        self.data_devolucao = timezone.now()
        self.livro.disponivel = True
        self.livro.save()
        self.save()