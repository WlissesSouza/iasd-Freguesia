from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import mimetypes


def validate_video_file(value):
    video_mime_type, _ = mimetypes.guess_type(value.name)
    if not video_mime_type or not video_mime_type.startswith('video/'):
        raise ValidationError('Só é permitido enviar arquivos de vídeo.')


class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    video_file = models.FileField(upload_to="videos/", verbose_name="Arquivo de Vídeo",
                                  validators=[validate_video_file],)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última atualização")  # Só esse campo

    class Meta:
        verbose_name = "Vídeo"
        verbose_name_plural = "Vídeos"

    def save(self, *args, **kwargs):
        Video.objects.all().delete()  # Mantém um único vídeo
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
