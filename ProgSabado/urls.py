from django.urls import path
from .views import listar_programacoes, detalhes_programacao

urlpatterns = [
    path('', listar_programacoes, name='listar_programacoes'),
    path('detalhe/<int:programacao_id>', detalhes_programacao, name='detalhes_programacao'),
]
