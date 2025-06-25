from http.client import HTTPResponse

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(response):
    return HttpResponse("hello django")
def new(response):
    return HttpResponse("new page")
def newfunction(response):
    return HttpResponse("newpage")