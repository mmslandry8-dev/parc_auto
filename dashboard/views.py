from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from accounts.decorators import (
    admin_required,
    agent_required
)

from vehicles.models import Vehicle

from rentals.models import Rental

from payments.models import Payment

from django.contrib.auth.models import User

from django.db.models import Sum

# Create your views here.

def home(request):
    """
    Page d'accueil du site
    """
    return render(request, 'home.html')

@login_required
@admin_required
def admin_dashboard(request):

    """
    Dashboard administrateur dynamique
    """

    # VEHICULES
    total_vehicles = Vehicle.objects.count()

    available_vehicles = Vehicle.objects.filter(
        statut='DISPONIBLE'
    ).count()

    rented_vehicles = Vehicle.objects.filter(
        statut='LOUE'
    ).count()

    # LOCATIONS
    total_rentals = Rental.objects.count()

    pending_rentals = Rental.objects.filter(
        statut='EN_ATTENTE'
    ).count()

    validated_rentals = Rental.objects.filter(
        statut='VALIDEE'
    ).count()

    # UTILISATEURS
    total_clients = User.objects.filter(
        groups__name='CLIENT'
    ).count()

    # REVENUS
    total_revenue = Payment.objects.filter(
        statut='PAYE'
    ).aggregate(
        Sum('montant')
    )['montant__sum']

    if total_revenue is None:

        total_revenue = 0

    context = {

        'total_vehicles': total_vehicles,

        'available_vehicles': available_vehicles,

        'rented_vehicles': rented_vehicles,

        'total_rentals': total_rentals,

        'pending_rentals': pending_rentals,

        'validated_rentals': validated_rentals,

        'total_clients': total_clients,

        'total_revenue': total_revenue,

    }

    return render(
        request,
        'dashboard/admin_dashboard.html',
        context
    )