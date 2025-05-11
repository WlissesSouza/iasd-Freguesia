from django.shortcuts import render
import requests
from django.conf import settings
from django.http import JsonResponse
from Boletim.models import Video


def video_boletim(request):
    video = Video.objects.first()  # Obtém o único vídeo (ou nenhum se não houver)
    return render(request, 'video_boletim.html', {'video': video})


def youtube_videos(request):
    api_key = settings.YOUTUBE_API_KEY
    channel_id = 'UClqKX3IggNnDhzct3kDRM7A'  # Use o ID correto
    max_results = 3

    url = (
        f'https://www.googleapis.com/youtube/v3/search?key={api_key}'
        f'&channelId={channel_id}&part=snippet,id&order=date&maxResults={max_results}'
    )

    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a resposta foi bem-sucedida (200 OK)
        data = response.json()

        # Depuração: imprime a resposta
        print(data)

        if "items" not in data or len(data["items"]) == 0:
            return JsonResponse({"error": "Nenhum vídeo encontrado ou o canal não tem vídeos recentes."}, status=404)

        live_video = None
        videos = []

        # Verifica se há transmissão ao vivo
        for item in data["items"]:
            if item["id"]["kind"] == "youtube#video":
                if 'liveBroadcastContent' in item['snippet'] and item['snippet']['liveBroadcastContent'] == 'live':
                    live_video = {
                        "title": item["snippet"]["title"],
                        "video_id": item["id"]["videoId"],
                        "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                        "live": True
                    }
                else:
                    videos.append({
                        "title": item["snippet"]["title"],
                        "video_id": item["id"]["videoId"],
                        "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                        "live": False
                    })

        # Se houver um vídeo ao vivo, o adiciona ao topo da lista
        if live_video:
            return JsonResponse({"videos": [live_video] + videos})

        return JsonResponse({"videos": videos})

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Erro ao se comunicar com a API do YouTube: {str(e)}"}, status=500)


def home(request):
    return render(request, 'home.html')
