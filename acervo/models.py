from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13, unique=True)
    ano_publicacao = models.IntegerField()
    editora = models.CharField(max_length=100)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"