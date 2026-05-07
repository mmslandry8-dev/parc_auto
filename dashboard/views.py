from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from accounts.decorators import (
    admin_required,
    agent_required
)
# Create your views here.

def home(request):
    """
    Page d'accueil du site
    """
    return render(request, 'home.html')

@login_required
@admin_required
def admin_dashboard(request):

    return render(
        request,
        'dashboard/admin_dashboard.html'
    )


@login_required
@agent_required
def agent_dashboard(request):

    return render(
        request,
        'dashboard/agent_dashboard.html'
    )