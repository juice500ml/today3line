import json

from . import views

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone

from main.parsecast import parse_link, get_list
from main.models import ParsedData

def index(req):
    return render(req, 'main/index.html', {'posts': ParsedData.objects.all()})
