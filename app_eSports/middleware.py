# app_eSports/middleware.py
from .models import SiteVisits
from django.db.models import F
from django.core.exceptions import ValidationError

class VisitCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se a sessão já foi contada E se não é admin/media/static
        # E se a sessão já foi iniciada (necessário para request.session funcionar)
        if hasattr(request, 'session') and not request.session.get('has_visited', False) and \
           not request.path.startswith('/admin/') and \
           not request.path.startswith('/media/') and \
           not request.path.startswith('/static/'):
            
            try:
                # Pega ou cria o contador
                visit_counter, created = SiteVisits.objects.get_or_create(pk=1, defaults={'count': 0})
                
                # Incrementa o contador
                SiteVisits.objects.filter(pk=1).update(count=F('count') + 1)
                
                # Marca a sessão como 'visitada' para não contar de novo
                request.session['has_visited'] = True
                
            except Exception: 
                # Ignora erros caso o banco não esteja pronto
                pass

        response = self.get_response(request)
        return response