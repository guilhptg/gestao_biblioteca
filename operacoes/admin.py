from django.contrib import admin
from .models import Emprestimo

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'livro', 'data_emprestimo', 'status')
    list_filter = ('status',)