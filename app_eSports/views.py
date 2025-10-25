# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Noticia, Produto, Partida, Jogador

# Views das Páginas Principais
def home_view(request):
    ultimas_noticias = Noticia.objects.order_by('-data_publicacao')[:3]
    proximas_partidas = Partida.objects.filter(status='agendada').order_by('data_hora')[:3]
    jogadores = Jogador.objects.all()
    context = {
        'noticias': ultimas_noticias,
        'partidas': proximas_partidas,
        'jogadores': jogadores
    }
    return render(request, 'app_eSports/home.html', context)

def noticias_list_view(request):
    noticias = Noticia.objects.order_by('-data_publicacao')
    return render(request, 'app_eSports/noticias_lista.html', {'noticias': noticias})

def noticia_detail_view(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    return render(request, 'app_eSports/noticia_detalhe.html', {'noticia': noticia})

def loja_view(request):
    produtos = Produto.objects.all()
    return render(request, 'app_eSports/loja.html', {'produtos': produtos})

def produto_detail_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'app_eSports/produto_detalhe.html', {'produto': produto})

def transmissao_view(request):
    # O link da transmissão pode ser salvo no BD ou fixo no template
    context = {'twitch_channel': 'alanzoka'} # Exemplo
    return render(request, 'app_eSports/transmissao.html', context)

# Views de Autenticação
def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'app_eSports/cadastro.html', {'form': form})

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
        form = AuthenticationForm()
    return render(request, 'app_eSports/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# Views do Carrinho (usando sessões)
def carrinho_view(request):
    carrinho = request.session.get('carrinho', {})
    produtos_ids = carrinho.keys()
    produtos_no_carrinho = Produto.objects.filter(id__in=produtos_ids)
    
    produtos_com_detalhes = []
    total_carrinho = 0
    
    for produto in produtos_no_carrinho:
        quantidade = carrinho[str(produto.id)]
        subtotal = produto.preco * quantidade
        produtos_com_detalhes.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })
        total_carrinho += subtotal

    return render(request, 'app_eSports/carrinho.html', {
        'produtos_com_detalhes': produtos_com_detalhes,
        'total_carrinho': total_carrinho
    })

def adicionar_ao_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id_str = str(produto_id)
    
    quantidade = int(request.POST.get('quantidade', 1))
    
    if produto_id_str in carrinho:
        carrinho[produto_id_str] += quantidade
    else:
        carrinho[produto_id_str] = quantidade
        
    request.session['carrinho'] = carrinho
    return redirect('carrinho')

def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id_str = str(produto_id)

    if produto_id_str in carrinho:
        del carrinho[produto_id_str]
    
    request.session['carrinho'] = carrinho
    return redirect('carrinho')