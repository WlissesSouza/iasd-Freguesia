from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # URL principal do app Home
    # path('api/youtube/', views.youtube_videos, name='youtube_videos'),
    path('boletim/', views.video_boletim, name='unique_video'),

]
