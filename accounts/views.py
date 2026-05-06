from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import RegisterForm

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
            group = Group.objects.get(name='CLIENT')
            user.groups.add(group)

            return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})