import json

from . import views

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone

from main.parsecast import parse_link, get_list
from main.models import Update

def index(req):
    return render(req, 'main/index.html')

def update(req):
    if req.method == 'POST':
        response = dict()

        if req.POST.get('first_time') == 'true':
            user_hash = req.POST.get('user_hash')
            print('First time conn by ' + str(user_hash))
            data = list()
            urls = get_list()
            for index in range(len(urls)):
                url = urls[index]
                param = parse_link(url)
                print('%d parsing done' % index)
                Update.objects.create(
                        user_hash = user_hash,
                        index = index,
                        title = param[0],
                        url = param[1],
                        image_url = param[2],
                        line1 = param[3][0],
                        line2 = param[3][1],
                        line3 = param[3][2]
                        )
            response['done'] = True
        else:
            user_hash = req.POST.get('user_hash')
            wanting_index = req.POST.get('index')
            for obj in Update.objects.filter(user_hash = user_hash).order_by('index'):
                if obj.index >= int(wanting_index):
                    response['new_one'] = True
                    response['title'] = obj.title
                    response['url'] = obj.url
                    response['image_url'] = obj.image_url
                    response['line1'] = obj.line1
                    response['line2'] = obj.line2
                    response['line3'] = obj.line3
                    break
                else:
                    response['new_one'] = False

            response['done'] = False

        return HttpResponse(json.dumps(response), content_type='application/json')
    return HttpResponseBadRequest()
