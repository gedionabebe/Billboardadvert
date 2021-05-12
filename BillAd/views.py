from django.http import HttpResponse
from django.shortcuts import render, redirect


def homepage(request):
    if request.user.is_authenticated:
        userr=request.user
        return render(request, 'homepage.html', {'userr': userr})
    else:
        return render(request, 'homepage.html')

def about(request):
    return render(request, 'about.html')



