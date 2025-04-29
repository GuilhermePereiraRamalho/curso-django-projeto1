from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("HOME")


def about(request):
    return HttpResponse("ABOUT")


def contact(request):
    return HttpResponse("CONTACT")
