from django.db import models
from django.utils import timezone

class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13, unique=True)
    ano_publicacao = models.IntegerField()
    editora = models.CharField(max_length=100)
    disponivel = models.BooleanField(default=True)
    ativo = models.BooleanField(default=True)  # Campo para controle de exclusão lógica
    data_exclusao = models.DateTimeField(null=True, blank=True, editable=False)  # Campo para armazenar data de exclusão lógica
    
    def editar_livro(self, titulo=None, autor=None, isbn=None, ano_publicacao=None, editora=None):
        """Método de encapsulamento para editar os detalhes do livro."""
        if titulo is not None:
            self.titulo = titulo
        if autor is not None:
            self.autor = autor
        if isbn is not None:
            self.isbn = isbn
        if ano_publicacao is not None:
            self.ano_publicacao = ano_publicacao
        if editora is not None:
            self.editora = editora
        self.save()
    
    def excluir_livro(self):
        """Método de encapsulamento para realizar exclusão lógica do livro."""
        self.ativo = False
        self.data_exclusao = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.titulo} - {self.autor}"