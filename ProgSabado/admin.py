from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.html import format_html
from ProgSabado.models import Programacao, ProgDetail
from .forms import ProgramacaoForm
MOMENTOS_PADRAO = [
    "Momento de Louvor",
    "Comunicação",
    "Louvor Especial",
    "Ofertório",
    "Hino Ofertório",
    "Oração ofertório",
    "Louvor Especial",
    "Momento Infantil",
    "Momento de Louvor",
    "Oração Intercessora",
    "Sermão",
    "Hino Final",
    "Oração Final",
    "Música Saída"
]


# Inline personalizado para ProgDetail
class ProgDetailInline(admin.TabularInline):
    model = ProgDetail
    extra = 0  # Não adicionar campos automaticamente
    readonly_fields = ['ordem', 'controls']  # Ordem e botões serão apenas leitura
    fields = ['ordem', 'momento', 'detalhe', 'obs', 'controls']  # Campos exibidos no inline
    ordering = ['ordem']  # Garante a ordenação no inline
    exclude = ['ordem']  # Esconde o campo

    def get_inlines(self, request, obj=None):
        if obj:  # Somente mostra os inlines ao editar
            return [ProgDetailInline]
        return []

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)

        # Se não tem detalhes ainda, cria automaticamente com base na lista padrão
        if obj and not obj.detalhes.exists():
            for index, momento in enumerate(MOMENTOS_PADRAO):
                ProgDetail.objects.create(
                    programacao=obj,
                    ordem=index + 1,
                    momento=momento
                )

        return super().change_view(request, object_id, form_url, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(f'/admin/ProgSabado/programacao/{obj.pk}/change/')

    def controls(self, obj):
        """
        Gera botões de controle apenas se o item não for o primeiro ou o último na ordem.
        """
        if not obj.id:  # Evita adicionar botões para objetos que ainda não foram salvos
            return ''

        # Obtenha os ids de menor e maior ordem
        first_detail = ProgDetail.objects.filter(programacao=obj.programacao).order_by('ordem').first()
        last_detail = ProgDetail.objects.filter(programacao=obj.programacao).order_by('ordem').last()

        # Verifique se este é o primeiro ou o último
        is_first = first_detail and obj.id == first_detail.id
        is_last = last_detail and obj.id == last_detail.id

        # Renderiza os botões relevantes
        buttons = ""
        if not is_first:
            buttons += f'<a class="button" style="margin-right: 5px;" href="{reverse("admin:progdetail_move_up", args=[obj.id])}">Subir</a>'
        if not is_last:
            buttons += f'<a class="button" href="{reverse("admin:progdetail_move_down", args=[obj.id])}">Descer</a>'

        return format_html(buttons)

    controls.short_description = 'Controles'


@admin.register(Programacao)
class ProgramacaoAdmin(admin.ModelAdmin):
    form = ProgramacaoForm
    list_display = ['data', 'anciao_do_dia']  # Exibe apenas a data na lista
    search_fields = ['data', 'anciao_do_dia']  # Permite busca por data
    inlines = [ProgDetailInline]

    def get_anciao_do_dia(self, obj):
        """
        Exibe o nome do usuário ou "Ninguém" no caso de campos nulos no admin.
        """
        return obj.anciao_do_dia.get_full_name() if obj.anciao_do_dia else "Ninguém"

    get_anciao_do_dia.short_description = 'Ancião do Dia'

    def get_urls(self):
        urls = super().get_urls()
        # Adiciona rotas customizadas para "subir" e "descer" ordem
        custom_urls = [
            path(
                'progdetail/<int:pk>/move-up/',
                self.admin_site.admin_view(self.move_up),
                name='progdetail_move_up',
            ),
            path(
                'progdetail/<int:pk>/move-down/',
                self.admin_site.admin_view(self.move_down),
                name='progdetail_move_down',
            ),
        ]
        return custom_urls + urls

    def move_up(self, request, pk):
        """
        Lógica para mover o ProgDetail para cima.
        """
        detalhe_atual = ProgDetail.objects.get(pk=pk)
        programacao = detalhe_atual.programacao
        detalhe_anterior = (
            ProgDetail.objects
            .filter(programacao=programacao, ordem__lt=detalhe_atual.ordem)
            .order_by('-ordem')
            .first()
        )
        if detalhe_anterior:
            # Trocar ordens
            detalhe_atual.ordem, detalhe_anterior.ordem = detalhe_anterior.ordem, detalhe_atual.ordem
            detalhe_atual.save()
            detalhe_anterior.save()

        # Redireciona de volta para a página de edição
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))

    def move_down(self, request, pk):
        """
        Lógica para mover o ProgDetail para baixo.
        """
        detalhe_atual = ProgDetail.objects.get(pk=pk)
        programacao = detalhe_atual.programacao

        detalhe_proximo = (
            ProgDetail.objects
            .filter(programacao=programacao, ordem__gt=detalhe_atual.ordem)
            .order_by('ordem')
            .first()
        )
        if detalhe_proximo:
            # Trocar ordens
            detalhe_atual.ordem, detalhe_proximo.ordem = detalhe_proximo.ordem, detalhe_atual.ordem
            detalhe_atual.save()
            detalhe_proximo.save()

        # Redireciona de volta para a página de edição
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """
        Sobrescreve a visualização do formulário de alteração para remover botões extras.
        """
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False  # Remove "Salvar e adicionar outro"
        extra_context['show_save_and_continue'] = False  # Remove "Salvar e continuar editando"
        extra_context['show_delete'] = False  # Remove botão "Excluir"
        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_inlines(self, request, obj):
        return [ProgDetailInline] if obj else []  # Somente exibe ao editar

    def save_model(self, request, obj, form, change):
        """
        Após criar a Programacao, cria os detalhes padrão se ainda não existirem.
        """
        super().save_model(request, obj, form, change)
        if not change and not obj.detalhes.exists():
            for index, momento in enumerate(MOMENTOS_PADRAO):
                ProgDetail.objects.create(
                    programacao=obj,
                    ordem=index + 1,
                    momento=momento
                )

    def response_add(self, request, obj, post_url_continue=None):
        # Redireciona para a edição assim que salvar uma nova Programacao
        return redirect(f'/admin/ProgSabado/programacao/{obj.pk}/change/')
