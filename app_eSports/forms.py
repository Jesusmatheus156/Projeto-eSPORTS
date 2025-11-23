# app_eSports/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# REMOVEMOS A IMPORTAÇÃO DO JOGADOR DAQUI
# from .models import Jogador 

class CustomUserCreationForm(UserCreationForm):
    # Campo de Email continua obrigatório
    email = forms.EmailField(required=True, help_text="Obrigatório. Digite um e-mail válido.")
    # REMOVEMOS o campo nickname daqui

    class Meta(UserCreationForm.Meta):
        model = User
        # Definimos os campos que vão aparecer no formulário (AGORA SEM NICKNAME)
        fields = ('username', 'email') 

    def save(self, commit=True):
        # Salva o usuário (username, email, senha)
        user = super().save(commit=False) # Pega o usuário sem salvar ainda
        user.email = self.cleaned_data['email'] # Adiciona o email
        
        # REMOVEMOS A CRIAÇÃO AUTOMÁTICA DO JOGADOR
        # if commit:
        #     user.save()
        #     # Linha REMOVIDA: Jogador.objects.create(usuario=user, nickname=nickname)
            
        # Agora só salva o usuário normal
        if commit:
            user.save()
            
        return user