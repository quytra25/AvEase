from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Hello World!")