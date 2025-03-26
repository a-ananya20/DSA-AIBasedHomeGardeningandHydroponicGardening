from django.shortcuts import render



def home(request):
    return render(request, 'home.html')


def home_gardening(request):
    return render(request, 'home_gardening.html')

def hydroponic_gardening(request):
    return render(request, 'hydroponic_gardening.html')