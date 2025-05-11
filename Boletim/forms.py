from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'publish_date']
        widgets = {
            'video_file': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }

    # Validando campos obrigatórios no formulário
    def clean(self):
        cleaned_data = super().clean()
        video_file = cleaned_data.get("video_file")
        publish_date = cleaned_data.get("publish_date")

        # Valida o campo de anexo como obrigatório
        if not video_file:
            self.add_error('video_file', 'O campo de anexo é obrigatório.')

        # Valida o campo de data como obrigatório
        if not publish_date:
            self.add_error('publish_date', 'O campo de data é obrigatório.')

        return cleaned_data
