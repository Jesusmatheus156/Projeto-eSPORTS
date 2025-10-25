# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Jogador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jogador')
    nickname = models.CharField(max_length=100)
    funcao = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: Estrategista, Ofensivo")

    def __str__(self):
        return self.nickname

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    imagem_destaque = models.ImageField(upload_to='noticias/', blank=True, null=True)

    def __str__(self):
        return self.titulo

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Partida(models.Model):
    STATUS_CHOICES = (
        ('agendada', 'Agendada'),
        ('finalizada', 'Finalizada'),
        ('ao_vivo', 'Ao Vivo'),
    )
    modalidade = models.CharField(max_length=50, default="Clash Royale")
    adversario = models.CharField(max_length=100)
    data_hora = models.DateTimeField()
    resultado = models.CharField(max_length=50, blank=True, null=True, help_text="Ex: 2-1")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendada')

    def __str__(self):
        return f"Clash Royale vs {self.adversario} em {self.data_hora.strftime('%d/%m/%Y')}"