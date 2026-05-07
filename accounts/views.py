from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import RegisterForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .utils import assign_user_role

def register(request):
    """
    Inscription d'un utilisateur CLIENT
    """
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Hash du mot de passe
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Ajouter au groupe CLIENT
            # group = Group.objects.get(name='CLIENT')
            # user.groups.add(group)
            # ROLE PAR DÉFAUT
            assign_user_role(user, 'CLIENT')

            return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """
    Connexion utilisateur
    """

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # REDIRECTION SELON RÔLE

            if user.groups.filter(name='ADMIN').exists():

                return redirect('admin_dashboard')

            elif user.groups.filter(name='AGENT').exists():

                return redirect('agent_dashboard')

            else:

                return redirect('home')

        else:

            messages.error(
                request,
                "Nom d'utilisateur ou mot de passe incorrect"
            )

    return render(request, 'accounts/login.html')

def logout_view(request):
    """
    Déconnexion utilisateur
    """

    logout(request)

    return redirect('home')