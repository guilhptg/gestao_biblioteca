from django.contrib import admin
from .models import Livro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'isbn', 'disponivel')
    search_fields = ('titulo', 'isbn')
    list_filter = ('disponivel',)