from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from accounts.decorators import (
    admin_required,
    agent_required
)

from vehicles.models import Vehicle

from rentals.models import Rental

from payments.models import Payment

from sales.models import Sale

from django.contrib.auth.models import User

from django.db.models import Sum

from django.db.models.functions import ExtractMonth

from django.db.models.functions import ExtractMonth

import json

# HOME
def home(request):

    """
    Page d'accueil du site
    """

    return render(
        request,
        'home.html'
    )


# DASHBOARD ADMIN
@login_required
@admin_required
def admin_dashboard(request):

    """
    Dashboard administrateur dynamique
    """

    # =========================
    # VEHICULES
    # =========================

    total_vehicles = Vehicle.objects.count()

    available_vehicles = Vehicle.objects.filter(
        statut='DISPONIBLE'
    ).count()

    rented_vehicles = Vehicle.objects.filter(
        statut='LOUE'
    ).count()

    sold_vehicles = Vehicle.objects.filter(
        statut='VENDU'
    ).count()

    # =========================
    # LOCATIONS
    # =========================

    total_rentals = Rental.objects.count()

    pending_rentals = Rental.objects.filter(
        statut='EN_ATTENTE'
    ).count()

    validated_rentals = Rental.objects.filter(
        statut='VALIDEE'
    ).count()

    # =========================
    # UTILISATEURS
    # =========================

    total_clients = User.objects.filter(
        groups__name='CLIENT'
    ).count()

    # =========================
    # REVENUS LOCATIONS
    # =========================

    rental_revenue = Payment.objects.filter(
        statut='PAYE'
    ).aggregate(
        Sum('montant')
    )['montant__sum']

    if rental_revenue is None:

        rental_revenue = 0

    # =========================
    # REVENUS VENTES
    # =========================

    sales_revenue = Sale.objects.filter(
        statut='PAYEE'
    ).aggregate(
        Sum('prix_vente')
    )['prix_vente__sum']

    if sales_revenue is None:

        sales_revenue = 0

    # =========================
    # REVENU TOTAL
    # =========================

    total_revenue = rental_revenue + sales_revenue

    # =========================
    # STATISTIQUES MENSUELLES
    # =========================

    monthly_payments = Payment.objects.filter(
        statut='PAYE'
    ).annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(
        total=Sum('montant')
    ).order_by('month')

    months = []
    totals = []

    for data in monthly_payments:

        months.append(data['month'])

        totals.append(float(data['total']))

    # =========================
    # CONTEXT
    # =========================

    context = {

        # VEHICULES
        'total_vehicles': total_vehicles,
        'available_vehicles': available_vehicles,
        'rented_vehicles': rented_vehicles,
        'sold_vehicles': sold_vehicles,

        # LOCATIONS
        'total_rentals': total_rentals,
        'pending_rentals': pending_rentals,
        'validated_rentals': validated_rentals,

        # CLIENTS
        'total_clients': total_clients,

        # REVENUS
        'rental_revenue': rental_revenue,
        'sales_revenue': sales_revenue,
        'total_revenue': total_revenue,

        # CHARTS
        'months': json.dumps(months),
        'totals': json.dumps(totals),
        # 'months': months,
        # 'totals': totals,

    }

    return render(
        request,
        'dashboard/admin_dashboard.html',
        context
    )

@login_required
@agent_required
def agent_dashboard(request):

    """
    Dashboard agent
    """

    # VEHICULES DISPONIBLES
    available_vehicles = Vehicle.objects.filter(
        statut='DISPONIBLE'
    ).count()

    # LOCATIONS EN ATTENTE
    pending_rentals = Rental.objects.filter(
        statut='EN_ATTENTE'
    ).count()

    # LOCATIONS VALIDÉES
    validated_rentals = Rental.objects.filter(
        statut='VALIDEE'
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

        'available_vehicles': available_vehicles,

        'pending_rentals': pending_rentals,

        'validated_rentals': validated_rentals,

        'total_revenue': total_revenue,

    }

    return render(
        request,
        'dashboard/agent_dashboard.html',
        context
    )