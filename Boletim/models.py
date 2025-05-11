from django.db import models
from django.core.exceptions import ValidationError
import mimetypes


def validate_video_file(value):
    # Obtém o tipo MIME do arquivo enviado
    video_mime_type, _ = mimetypes.guess_type(value.name)

    # Verifica se o tipo MIME começa com "video/"
    if not video_mime_type or not video_mime_type.startswith('video/'):
        raise ValidationError('Só é permitido enviar arquivos de vídeo.')


class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    video_file = models.FileField(upload_to="videos/", verbose_name="Arquivo de Vídeo",
                                  validators=[validate_video_file])
    publish_date = models.DateField(verbose_name="Data de Publicação")

    class Meta:
        verbose_name = "Vídeo"
        verbose_name_plural = "Vídeos"

    def save(self, *args, **kwargs):
        # Antes de salvar, apagamos qualquer vídeo existente no banco
        Video.objects.all().delete()
        super(Video, self).save(*args, **kwargs)  # Salvamos o novo vídeo

    def __str__(self):
        return self.title
