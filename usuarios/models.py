from django.db import models


class Usuario(models.Model):
    __table_name__ = 'usuarios'  # Nome explícito da tabela para clareza e controle
    # O Django já cria um ID auto-incremental automaticamente
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=20, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

    @property
    def limite_emprestimo(self) -> int:
        """Propriedade base que será sobreposta pelas subclasses (Polimorfismo)"""
        return 0

class Aluno(Usuario):
    # Herança multi-tabela: cria uma tabela própria vinculada a Usuario
    curso = models.CharField(max_length=100)

    @property
    def limite_emprestimo(self) -> int:
        return 3  # Regra de negócio específica para Alunos

class Professor(Usuario):
    departamento = models.CharField(max_length=100)

    @property
    def limite_emprestimo(self) -> int:
        return 5  # Regra de negócio específica para Professores