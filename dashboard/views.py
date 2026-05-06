from django.shortcuts import render

# Create your views here.

def home(request):
    """
    Page d'accueil du site
    """
    return render(request, 'home.html')