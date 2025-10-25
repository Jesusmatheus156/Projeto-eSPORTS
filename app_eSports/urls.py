# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Páginas principais
    path('', views.home_view, name='home'),
    path('noticias/', views.noticias_list_view, name='noticias_lista'),
    path('noticias/<int:pk>/', views.noticia_detail_view, name='noticia_detalhe'),
    path('loja/', views.loja_view, name='loja'),
    path('produto/<int:pk>/', views.produto_detail_view, name='produto_detalhe'),
    path('transmissao/', views.transmissao_view, name='transmissao'),

    # Autenticação
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Carrinho (lógica, sem template próprio)
    path('carrinho/', views.carrinho_view, name='carrinho'),
    path('adicionar-ao-carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover-do-carrinho/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
]