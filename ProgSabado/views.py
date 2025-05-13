from django.shortcuts import render, get_object_or_404
from .models import Programacao, ProgDetail


# View para listar todas as programações
def listar_programacoes(request):
    programacoes = Programacao.objects.order_by('-data')  # Ordena pela data, mais recente primeiro
    return render(request, 'listar_programacoes.html', {'programacoes': programacoes})


# View para exibir os detalhes de uma programação específica
def detalhes_programacao(request, programacao_id):
    programacao = get_object_or_404(Programacao, id=programacao_id)
    detalhes = programacao.detalhes.order_by('ordem')  # Ordena pelo campo 'ordem'
    return render(request, 'detalhes_programacao.html', {'programacao': programacao, 'detalhes': detalhes})
