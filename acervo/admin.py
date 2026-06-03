from django.contrib import admin
from acervo.models import Livro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'isbn', 'disponivel')
    search_fields = ('titulo', 'isbn')
    list_filter = ('disponivel',)