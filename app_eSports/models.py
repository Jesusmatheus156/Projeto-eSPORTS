# app_eSports/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from decimal import Decimal

class Jogador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jogador')
    nickname = models.CharField(max_length=100)
    # funcao = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: Estrategista, Ofensivo") # Comentado/Removido
    
    imagem = models.ImageField(upload_to='jogadores/', blank=True, null=True, help_text="Foto do jogador (formato quadrado)")
    # CORREÇÃO: Removido espaço extra da linha abaixo
    nivel_cr = models.PositiveIntegerField(blank=True, null=True, verbose_name="Nível (Clash Royale)") 
    trofeus_cr = models.PositiveIntegerField(blank=True, null=True, verbose_name="Troféus (Clash Royale)")
    cla = models.CharField(max_length=100, blank=True, null=True, verbose_name="Clã (Clash Royale)")

    def __str__(self):
        return self.nickname
    
    class Meta:
         verbose_name = "Jogador da Equipe"
         verbose_name_plural = "Jogadores da Equipe"

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: 'Atualizações', 'Competitivo'")
    resumo = models.TextField(max_length=300, help_text="Um parágrafo curto que aparece na home e na lista de notícias.")
    conteudo = RichTextUploadingField(verbose_name="Conteúdo da Matéria")
    data_publicacao = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagem_destaque = models.ImageField(upload_to='noticias_destaques/', blank=True, null=True)

    def __str__(self):
        return self.titulo

class Produto(models.Model):
    nome = models.CharField(max_length=100) 
    descricao = models.TextField()
    is_lancamento = models.BooleanField(default=False, verbose_name="É Lançamento?")
    
    def __str__(self):
        return self.nome

class VariacaoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='variacoes')
    nome = models.CharField(max_length=100, help_text="Ex: Branca, M") 
    
    # --- PREÇOS ATUALIZADOS ---
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Atual")
    preco_antigo = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, 
        verbose_name="Preço Antigo (Riscado)",
        help_text="Deixe em branco se não houver desconto."
    )
    max_parcelas_sem_juros = models.IntegerField(
        default=1, verbose_name="Nº de parcelas sem juros",
        help_text="Coloque 1 se não houver parcelamento sem juros"
    )
    frete_gratis = models.BooleanField(default=False, verbose_name="Tem frete grátis?")
    # --- FIM DOS CAMPOS NOVOS ---
    
    estoque = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Variação de Produto"
        verbose_name_plural = "Variações de Produto"

    def __str__(self):
        return f"{self.produto.nome} ({self.nome})"

    # --- PROPRIEDADES MÁGICAS (para usar no HTML) ---
    
    @property
    def porcentagem_off(self):
        """Calcula o desconto percentual"""
        if self.preco_antigo and self.preco_antigo > self.preco:
            desconto = self.preco_antigo - self.preco
            porcentagem = (desconto / self.preco_antigo) * 100
            return int(porcentagem) # Retorna o número inteiro (ex: 28)
        return 0

    @property
    def valor_parcela(self):
        """Calcula o valor da parcela"""
        if self.max_parcelas_sem_juros > 1:
            # Arredonda para 2 casas decimais
            return (self.preco / Decimal(self.max_parcelas_sem_juros)).quantize(Decimal('0.01'))
        return self.preco

class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='produtos/')
    legenda = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: Vista frontal (Branca)")

    class Meta:
        verbose_name = "Imagem de Produto"
        verbose_name_plural = "Imagens de Produto"

    def __str__(self):
        return f"Imagem de {self.produto.nome}"

class Partida(models.Model):
    """
    Controla TUDO:
    1. A AGENDA (Agendada)
    2. O PLAYER PRINCIPAL (Ao Vivo)
    3. O GRID DE VODS (Finalizada)
    """
    STATUS_CHOICES = (
        ('agendada', 'Agendada'),
        ('finalizada', 'Finalizada'),
        ('ao_vivo', 'Ao Vivo'),
    )
    
    modalidade = models.CharField(max_length=50, default="Clash Royale")
    adversario = models.CharField(max_length=100)
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendada',
                              help_text="Mude para 'Ao Vivo' para esta partida aparecer no Player Principal.")
    resultado = models.CharField(max_length=50, blank=True, null=True, help_text="Ex: 2-1")
    
    # --- Player Principal (QUANDO 'AO VIVO') ---
    iframe_live = models.TextField(
        blank=True, null=True, 
        verbose_name="Código Iframe da Live (Player Principal)",
        help_text="""
        Cole o <iframe> COMPLETO aqui (YouTube ou Twitch). 
        IMPORTANTE: Apague o width/height e adicione 
        style='position: absolute; top: 0; left: 0; width: 100%; height: 100%;'
        """
    )

    # --- VODs (QUANDO 'FINALIZADA') ---
    link_vod = models.URLField(blank=True, null=True, 
                               verbose_name="Link do VOD (Gravação)",
                               help_text="Link completo da gravação (VOD) após a partida ser 'Finalizada'.")
    thumbnail_vod = models.ImageField(upload_to='partidas_thumbnails/', blank=True, null=True, 
                                      verbose_name="Thumbnail do VOD (Capa do Card)")
    
    class Meta:
        ordering = ['data_hora']
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"

    def __str__(self):
        return f"{self.modalidade} vs {self.adversario} em {self.data_hora.strftime('%d/%m/%Y')}"

class SiteVisits(models.Model):
    count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk and SiteVisits.objects.exists():
            # Apenas impede a criação, não levanta erro que quebra
            print("AVISO: Tentativa de criar segunda instância de SiteVisits ignorada.") 
            return 
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Total de Visitas: {self.count}"
    
    class Meta:
        verbose_name = "Visitas do Site"
        verbose_name_plural = "Visitas do Site"