from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']
        widgets = {
            'video_file': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define um valor inicial para o campo no formulário renderizado
        if self.fields['title'].initial is None:
            self.fields['title'].initial = "Boletim"


    # Validando campos obrigatórios no formulário
    def clean(self):
        cleaned_data = super().clean()
        video_file = cleaned_data.get("video_file")

        # Valida o campo de anexo como obrigatório
        if not video_file:
            self.add_error('video_file', 'O campo de anexo é obrigatório.')

        return cleaned_data
