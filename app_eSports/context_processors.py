# app_eSports/context_processors.py
from django.contrib.auth.models import User
from .models import SiteVisits
from .models import Partida

def site_stats(request):
    total_users = User.objects.count()
    
    # Tenta pegar as visitas, se não existir (primeira vez), retorna 0
    try:
        total_visits = SiteVisits.objects.get(pk=1).count
    except SiteVisits.DoesNotExist:
        total_visits = 0
        
    return {
        'total_users': total_users,
        'total_visits': total_visits,
    }


def live_status_processor(request):
    """A 'Fonte da Verdade Única' para a live principal."""
    partida_ao_vivo_global = Partida.objects.filter(status='ao_vivo').order_by('data_hora').first()
    return {
        'partida_ao_vivo_global': partida_ao_vivo_global
    }