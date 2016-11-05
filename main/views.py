import json

from . import views

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone

from main.parsecast import parse_link, get_list
from main.models import ParsedData

def index(req):
    return render(req, 'main/index.html')

def update(req):
    if req.method == 'POST':
        response = dict()

        if req.POST.get('first_time') == 'true':
            urls = get_list()
            for url in urls:
                if not ParsedData.objects.filter(url = url):
                    ParsedData.objects.create(
                            url = url,
                            title = '',
                            image_url = '',
                            line1 = '',
                            line2 = '',
                            line3 = '',
                            dirty = False,
                            )
            response['url_list'] = json.dumps(urls)
        else:
            wanting_url = req.POST.get('url')
            print(wanting_url)
            obj = ParsedData.objects.filter(url = wanting_url)[0]
            if not obj.dirty:
                obj.dirty = True
                obj.save()

                param = parse_link(wanting_url)
                obj.title = param[0]
                obj.image_url = param[2]
                obj.line1 = param[3][0]
                obj.line2 = param[3][1]
                obj.line3 = param[3][2]
                obj.save()

            response['title'] = obj.title
            response['url'] = obj.url
            response['image_url'] = obj.image_url
            response['line1'] = obj.line1
            response['line2'] = obj.line2
            response['line3'] = obj.line3

        return HttpResponse(json.dumps(response), content_type='application/json')
    return HttpResponseBadRequest()
