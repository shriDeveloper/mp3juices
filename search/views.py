import youtube_dl
import os
import re
from youtube_search import YoutubeSearch
from django.http import HttpResponse,Http404,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render,redirect
def search(request):
    query=request.GET.get("song_id")
    if query is None:
        return redirect('/')
    song_name=request.GET.get('short_hand')
    result=request.GET.get('unique_hash')
    ydl_opts = {
    'format': 'worstaudio/worst',
    'postprocessors': [{'key': 'FFmpegExtractAudio',
               'preferredcodec': 'mp3',
               'preferredquality': '192'}],
    'outtmpl': 'media/'+result,
    'noplaylist':True,
    'ignoreerrors':True,
    'max-downloads':1,
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    try:
        ydl.download([query])
    except  youtube_dl.utils.DownloadError:
        return render(request,'homepage/index_new.html',{'ERROR':"This Songs is not available in your country."})
    file_path = os.path.join(settings.MEDIA_ROOT, result)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse("ec2-18-223-136-205.us-east-2.compute.amazonaws.com/media/"+fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + song_name
            return response
    raise Http404
@csrf_exempt
def autosuggest(request):
    data = request.GET.get("term")
    if data is None:
        return redirect('/')
    results=[]
    while not results:
        results = YoutubeSearch(''+data, max_results=5).to_dict()
    for result in results:
        title=re.sub('[\W_]+','',str(result['title']),flags=re.ASCII)
        result['short_hand']=title+".mp3"
    return JsonResponse({"results":results},safe=False)
