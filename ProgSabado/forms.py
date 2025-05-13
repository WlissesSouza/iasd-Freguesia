from django import forms
from django.contrib.auth.models import User
from .models import Programacao

class ProgramacaoForm(forms.ModelForm):
    class Meta:
        model = Programacao
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tornar o campo 'anciao_do_dia' somente leitura após a seleção
        if 'anciao_do_dia' in self.fields:
            self.fields['anciao_do_dia'].widget.attrs['disabled'] = 'disabled'  # Desabilita o campo
            self.fields['anciao_do_dia'].widget.can_delete_related = False  # Remove opção de deletar
            self.fields['anciao_do_dia'].widget.can_change_related = False  # Remove opção de editar
            self.fields['anciao_do_dia'].widget.can_add_related = False  # Remove opção de adicionar novos usuários

