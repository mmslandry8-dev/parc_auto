from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import RegisterForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .utils import assign_user_role

from customers.models import Customer


from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegisterForm

from .utils import assign_user_role

from customers.models import Customer


def register(request):

    """
    Inscription d'un utilisateur CLIENT
    """

    # Formulaire vide
    form = RegisterForm()

    # Si formulaire soumis
    if request.method == 'POST':

        form = RegisterForm(request.POST)

        # Vérification validité
        if form.is_valid():

            # Création utilisateur sans sauvegarde immédiate
            user = form.save(commit=False)

            # Hash sécurisé mot de passe
            user.set_password(
                form.cleaned_data['password']
            )

            # Sauvegarde user
            user.save()

            # Attribution rôle CLIENT
            assign_user_role(user, 'CLIENT')

            # Création fiche client automatique
            Customer.objects.create(

                user=user,

                nom=user.username,

                email=user.email

            )

            messages.success(
                request,
                "Compte créé avec succès."
            )

            return redirect('login')

        else:

            messages.error(
                request,
                "Veuillez corriger les erreurs."
            )

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


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