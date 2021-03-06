import youtube_dl
import os
import re
import uuid
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render,redirect
def search(request):
    query=request.GET.get("term")
    if query is None:
        return redirect('/')
    result=str(uuid.uuid1())+'.mp3'
    ydl_opts = {
    'format': 'worstaudio/worst',
    'postprocessors': [{'key': 'FFmpegExtractAudio',
               'preferredcodec': 'mp3',
               'preferredquality': '192'}],
    'outtmpl': 'media/'+result,
    'noplaylist':True,
    'ignoreerrors':True,
    'max-downloads':1,
    '--external-downloader':'aria2c',
    '--external-downloader-args':'-c 8 -x 8 -s 8 -k 1M',
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(query, download=True)
    title=re.sub('[\W_]+','',str(info_dict['title']),flags=re.ASCII)
    file_path = os.path.join(settings.MEDIA_ROOT, result)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename='+title+'.mp3'
            return response
    raise Http404
