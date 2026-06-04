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
    
    def editar_usuario(self, nome: str = None, email: str = None, ativo: bool = None):
        """Método para editar os dados do usuário"""
        if nome is not None:
            self.nome = nome
        if email is not None:
            self.email = email
        if ativo is not None:
            self.ativo = ativo
        self.save()
    
    @property
    def tipo_usuario(self) -> str:
        """Retorna o tipo real do usuário para o template"""
        if hasattr(self, 'aluno'):
            return 'Aluno'
        if hasattr(self, 'professor'):
            return 'Professor'
        return 'Administrador'
    
    def excluir_usuario(self):
        """Método para excluir o usuário (soft delete)"""
        self.ativo = False
        self.save()

class Aluno(Usuario):
    # Herança multi-tabela: cria uma tabela própria vinculada a Usuario
    curso = models.CharField(max_length=100)

    @property
    def limite_emprestimo(self) -> int:
        return 3  # Regra de negócio específica para Alunos
    
    def alterar_curso(self, novo_curso: str):
        """Método específico para alterar o curso do aluno"""
        self.curso = novo_curso
        self.save()

class Professor(Usuario):
    departamento = models.CharField(max_length=100)

    @property
    def limite_emprestimo(self) -> int:
        return 5  # Regra de negócio específica para Professores
    
    def alterar_departamento(self, novo_departamento: str):
        """Método específico para alterar o departamento do professor"""
        self.departamento = novo_departamento
        self.save()