from django.contrib import admin
from .models import Video
from .forms import VideoForm


class VideoAdmin(admin.ModelAdmin):
    form = VideoForm


admin.site.register(Video, VideoAdmin)
