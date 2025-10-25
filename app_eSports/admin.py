# core/admin.py
from django.contrib import admin
from .models import Jogador, Noticia, Produto, Partida

@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'usuario', 'funcao')

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_publicacao')
    list_filter = ('autor', 'data_publicacao')
    search_fields = ('titulo', 'conteudo')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque')
    search_fields = ('nome',)

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('adversario', 'data_hora', 'status', 'resultado')
    list_filter = ('status', 'data_hora')