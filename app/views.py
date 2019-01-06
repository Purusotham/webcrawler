from django.shortcuts import render
from django.http.response import HttpResponse
from app.handlers.spyder import WebCrawler
from json import loads as json_loads, dumps as json_dumps
from traceback import format_exc
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def parse_html(request):
    try:
        data = json_loads(request.body)
        response = WebCrawler(data.get('url', ''),
                              data.get('depth', 1)).spiderbot()
        return HttpResponse(json_dumps(response))
    except Exception as error:
        print('Exception in parse_html...:' + str(error))
        print(format_exc().splitlines())
        return HttpResponse(json_dumps({'status_id': 0,
                                        'reason': 'Failed while getting url'}))
