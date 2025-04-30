from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'recipes/home.html', context={
        'name': 'Guilherme'
    })


def about(request):
    return render(request, 'me-apague/temp.html')


def contact(request):
    return HttpResponse("CONTACT")
