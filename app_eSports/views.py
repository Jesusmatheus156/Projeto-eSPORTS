# app_eSports/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Noticia, Produto, Partida, Jogador, VariacaoProduto
from .forms import CustomUserCreationForm
from django.db.models import Q 

def home_view(request):
    ultimas_noticias = Noticia.objects.order_by('-data_publicacao')[:3]
    proximas_partidas = Partida.objects.filter(status='agendada').order_by('data_hora')[:3]
    jogadores = Jogador.objects.all()
    lancamentos = Produto.objects.filter(is_lancamento=True).prefetch_related('imagens', 'variacoes')[:3] # Pega até 3 lançamentos
    context = {
        'noticias': ultimas_noticias,
        'partidas': proximas_partidas,
        'jogadores': jogadores,
        'lancamentos': lancamentos,
    }
    return render(request, 'app_eSports/home.html', context)

def noticias_list_view(request):
    noticias = Noticia.objects.order_by('-data_publicacao')
    return render(request, 'app_eSports/noticias_lista.html', {'noticias': noticias})

def noticia_detail_view(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    return render(request, 'app_eSports/noticia_detalhe.html', {'noticia': noticia})

def loja_view(request):
    produtos = Produto.objects.prefetch_related('imagens', 'variacoes').all()
    return render(request, 'app_eSports/loja.html', {'produtos': produtos})

def produto_detail_view(request, pk):
    # Usamos o prefetch_related de novo
    produto = get_object_or_404(
        Produto.objects.prefetch_related('imagens', 'variacoes'), 
        pk=pk
    )
    return render(request, 'app_eSports/produto_detalhe.html', {'produto': produto})

def transmissao_view(request):
    context = {'twitch_channel': 'alanzoka'} # Exemplo
    return render(request, 'app_eSports/transmissao.html', context)

def pesquisa_view(request):
    query = request.GET.get('q', '') 
    
    produtos_encontrados = Produto.objects.none()
    noticias_encontradas = Noticia.objects.none()

    if query:
        produtos_encontrados = Produto.objects.filter(
            Q(nome__icontains=query) | Q(descricao__icontains=query)
        ).distinct().prefetch_related('imagens', 'variacoes')
        
        noticias_encontradas = Noticia.objects.filter(
            Q(titulo__icontains=query) | Q(conteudo__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'produtos': produtos_encontrados,
        'noticias': noticias_encontradas
    }
    return render(request, 'app_eSports/pesquisa_resultados.html', context)

def cadastro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'app_eSports/autenticacao.html', {
        'cadastro_form': form,
        'form_type': 'cadastro'
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
             messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'app_eSports/autenticacao.html', {
        'login_form': form,
        'form_type': 'login'
    })

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required 
def perfil_view(request):
    # Reutiliza a lógica da view do carrinho
    context = _get_carrinho_context(request)
    return render(request, 'app_eSports/perfil.html', context)

# Função helper para não repetir código
def _get_carrinho_context(request):
    # O carrinho agora salva { 'variacao_id': quantidade }
    carrinho = request.session.get('carrinho', {})
    
    variacoes_ids = carrinho.keys()
    
    # Buscamos as variações no banco, já selecionando o produto
    variacoes_no_carrinho = VariacaoProduto.objects.filter(id__in=variacoes_ids).select_related('produto')
    
    produtos_com_detalhes = []
    total_carrinho = 0
    
    for variacao in variacoes_no_carrinho:
        quantidade = carrinho[str(variacao.id)]
        subtotal = variacao.preco * quantidade
        produtos_com_detalhes.append({
            'variacao': variacao, # Passamos a variação inteira
            'produto': variacao.produto, # Passamos o produto pai
            'quantidade': quantidade,
            'subtotal': subtotal,
            'imagem': variacao.produto.imagens.first() # Pega a primeira imagem do produto pai
        })
        total_carrinho += subtotal

    return {
        'produtos_com_detalhes': produtos_com_detalhes,
        'total_carrinho': total_carrinho
    }


def carrinho_view(request):
    context = _get_carrinho_context(request)
    return render(request, 'app_eSports/carrinho.html', context)


@login_required(login_url='login') # <--- ADICIONADO! Redireciona para o login se não estiver logado
def adicionar_ao_carrinho(request):
    if request.method != 'POST':
        return redirect('loja')

    carrinho = request.session.get('carrinho', {})
    
    # Pegamos os dados do formulário
    variacao_id = request.POST.get('variacao_id')
    quantidade = int(request.POST.get('quantidade', 1))

    if not variacao_id:
        messages.error(request, 'Selecione uma variação do produto.')
        # Tenta voltar para a página anterior, ou para a loja
        return redirect(request.META.get('HTTP_REFERER', 'loja'))

    try:
        variacao = VariacaoProduto.objects.get(id=variacao_id, estoque__gte=quantidade)
    except VariacaoProduto.DoesNotExist:
        messages.error(request, 'Produto ou variação indisponível no estoque.')
        return redirect(request.META.get('HTTP_REFERER', 'loja'))

    # Adiciona no carrinho
    if variacao_id in carrinho:
        carrinho[variacao_id] += quantidade
    else:
        carrinho[variacao_id] = quantidade
        
    request.session['carrinho'] = carrinho
    messages.success(request, f'"{variacao.produto.nome} ({variacao.nome})" adicionado ao carrinho!')
    return redirect('carrinho')

def remover_do_carrinho(request, variacao_id):
    carrinho = request.session.get('carrinho', {})
    variacao_id_str = str(variacao_id)

    if variacao_id_str in carrinho:
        del carrinho[variacao_id_str]
    
    request.session['carrinho'] = carrinho
    return redirect('carrinho')

def sobre_view(request):
    context = {} 
    return render(request, 'app_eSports/sobre.html', context)

# app_eSports/views.py
from django.shortcuts import render
from django.utils import timezone
from .models import Partida, Noticia, Jogador # ... etc

# ... (Sua view 'home', 'noticias', 'loja', etc. ficam aqui) ...

def agenda(request):
    agora = timezone.now()
    
    # O Context Processor já está buscando a partida ao vivo.
    # Esta view só precisa buscar as próximas e as finalizadas.
    
    proximas_partidas = Partida.objects.filter(
        status='agendada', 
        data_hora__gte=agora
    ).order_by('data_hora')
    
    ultimos_resultados = Partida.objects.filter(
        status='finalizada'
    ).order_by('-data_hora')[:10]

    context = {
        # REMOVEMOS 'partidas_ao_vivo' daqui
        'proximas_partidas': proximas_partidas,
        'ultimos_resultados': ultimos_resultados,
    }
    return render(request, 'app_eSports/agenda.html', context)


def transmissao(request):
    # O context_processor (partida_ao_vivo_global) já cuida da live principal.
    # Esta view só precisa buscar os VODs (Transmissões Anteriores).
    
    transmissoes_anteriores = Partida.objects.filter(
        status='finalizada',         # Só partidas finalizadas
        link_vod__isnull=False,      # Que tenham um link de VOD
    ).exclude(link_vod__exact='').order_by('-data_hora')[:8] # Pega as 8 últimas

    context = {
        'transmissoes_anteriores': transmissoes_anteriores,
        # REMOVEMOS 'outros_streams' daqui
        'request': request, 
    }
    return render(request, 'app_eSports/transmissao.html', context)

def classificacao_csi(request):
    # Adicionando esta view de volta (estava faltando, causando erro)
    return render(request, 'app_eSports/classificacao_csi.html')