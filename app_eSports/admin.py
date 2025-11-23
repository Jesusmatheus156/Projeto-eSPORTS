# app_eSports/admin.py
from django.contrib import admin
# CORREÇÃO: Garante que todos os modelos, incluindo SiteVisits, são importados PRIMEIRO
from .models import ( 
    Jogador, Noticia, Produto, Partida, 
    VariacaoProduto, ImagemProduto, SiteVisits 
)

@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin): 
    # CORREÇÃO: Remove 'funcao', adiciona 'cla'
    list_display = ('nickname', 'usuario', 'cla', 'nivel_cr', 'trofeus_cr') 
    # CORREÇÃO: Remove 'funcao', adiciona 'cla'
    fields = ('usuario', 'nickname', 'cla', 'imagem', 'nivel_cr', 'trofeus_cr') 

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_publicacao')
    list_filter = ('autor', 'data_publicacao')
    search_fields = ('titulo', 'conteudo')

class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

class VariacaoProdutoInline(admin.StackedInline):
    model = VariacaoProduto
    extra = 1
    # Organiza os campos no admin
    fieldsets = (
        (None, {
            'fields': ('nome', 'estoque')
        }),
        ('Preços e Condições (Estilo Mercado Livre)', {
            # Organiza os preços como você quer
            'fields': ('preco_antigo', 'preco', 'max_parcelas_sem_juros', 'frete_gratis')
        }),
    )
    
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # ADICIONE 'is_lancamento' AQUI
    list_display = ('nome', 'is_lancamento') 
    search_fields = ('nome',)
    inlines = [VariacaoProdutoInline, ImagemProdutoInline]
    list_filter = ('is_lancamento',) 
    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'is_lancamento')
        }),
    )


@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    # Botão de Salvar no TOPO da página
    save_on_top = True
    
    list_display = ('adversario', 'data_hora', 'status', 'resultado')
    list_filter = ('status', 'modalidade', 'data_hora')
    search_fields = ('adversario', 'modalidade')
    list_editable = ('resultado',) 
    
    # Organiza a página de edição em seções CLARAS
    fieldsets = (
        # Seção 1: Infos da Agenda
        ('1. Informações da Partida (Para a Agenda)', {
            'fields': ('modalidade', 'adversario', 'data_hora', 'status', 'resultado')
        }),
        # Seção 2: O Player Principal
        ('2. Player Principal (Se Status = "Ao Vivo")', {
            'description': "Preencha isto para o player principal da página /transmissao.",
            'fields': ('iframe_live',)
        }),
        # Seção 3: O Grid de VODs
        ('3. VOD (Se Status = "Finalizada")', {
            'description': "Preencha isto para o card de VOD na página /transmissao.",
            'fields': ('link_vod', 'thumbnail_vod')
        }),
    )

# CORREÇÃO: Agora SiteVisits já foi importado acima
@admin.register(SiteVisits)
class SiteVisitsAdmin(admin.ModelAdmin):
    list_display = ('id', 'count')
    # Impede a criação de novas instâncias pelo admin
    def has_add_permission(self, request):
        return not SiteVisits.objects.exists()