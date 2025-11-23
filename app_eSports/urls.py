# app_eSports/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Páginas principais
    path('', views.home_view, name='home'),
    path('noticias/', views.noticias_list_view, name='noticias_lista'),
    path('noticias/<int:pk>/', views.noticia_detail_view, name='noticia_detalhe'),
    path('loja/', views.loja_view, name='loja'),
    path('produto/<int:pk>/', views.produto_detail_view, name='produto_detalhe'),
    path('transmissao/', views.transmissao_view, name='transmissao'),
    path('pesquisa/', views.pesquisa_view, name='pesquisa'),
    path('sobre/', views.sobre_view, name='sobre'), # <-- NOVA LINHA

    # Autenticação
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),

    # ... (URLs de Recuperação de Senha) ...
        # URLs de Recuperação de Senha (Usando views nativas do Django)
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='app_eSports/autenticacao.html'), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='app_eSports/password_reset_done.html'), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='app_eSports/password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='app_eSports/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # Carrinho (URLs ATUALIZADAS)
    path('carrinho/', views.carrinho_view, name='carrinho'),
    # Não precisa mais de ID na URL, pegamos do formulário
    path('adicionar-ao-carrinho/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'), 
    # Agora removemos pela VARIACAO_ID
    path('remover-do-carrinho/<int:variacao_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),

    path('agenda/', views.agenda, name='agenda'),
    path('csi/', views.classificacao_csi, name='classificacao_csi'),
    path('transmissao/', views.transmissao, name='transmissao'),
]