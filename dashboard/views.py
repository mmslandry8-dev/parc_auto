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

from django.db.models.functions import TruncMonth

from django.db.models.functions import ExtractMonth

import json

from django.http import JsonResponse

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
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse

from payments.models import Payment
from rentals.models import Rental
from sales.models import Sale
from vehicles.models import Vehicle


@login_required
@admin_required
def admin_dashboard(request):

    """
    Dashboard administrateur dynamique + analytics
    """

    # =========================
    # VEHICULES
    # =========================
    total_vehicles = Vehicle.objects.count()
    available_vehicles = Vehicle.objects.filter(statut='DISPONIBLE').count()
    rented_vehicles = Vehicle.objects.filter(statut='LOUE').count()
    sold_vehicles = Vehicle.objects.filter(statut='VENDU').count()

    # =========================
    # LOCATIONS
    # =========================
    total_rentals = Rental.objects.count()
    pending_rentals = Rental.objects.filter(statut='EN_ATTENTE').count()
    validated_rentals = Rental.objects.filter(statut='VALIDEE').count()

    # =========================
    # VENTES
    # =========================
    total_sales = Sale.objects.count()
    pending_sales = Sale.objects.filter(statut='EN_ATTENTE').count()
    paid_sales = Sale.objects.filter(statut='PAYEE').count()

    # =========================
    # CLIENTS
    # =========================
    total_clients = User.objects.filter(groups__name='CLIENT').count()

    # =========================
    # REVENUS TOTAUX
    # =========================
    rental_revenue = Payment.objects.filter(
        statut='PAYE',
        rental__isnull=False
    ).aggregate(Sum('montant'))['montant__sum'] or 0

    sales_revenue = Payment.objects.filter(
        statut='PAYE',
        rental__isnull=True
    ).aggregate(Sum('montant'))['montant__sum'] or 0

    total_revenue = rental_revenue + sales_revenue

    # =========================
    # REVENUS MENSUELS (CHART)
    # =========================
    monthly_data = Payment.objects.filter(
        statut='PAYE'
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total=Sum('montant')
    ).order_by('month')

    months = []
    totals = []

    for item in monthly_data:
        months.append(item['month'].strftime("%Y-%m"))
        totals.append(float(item['total']))

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

        # VENTES
        'total_sales': total_sales,
        'pending_sales': pending_sales,
        'paid_sales': paid_sales,

        # CLIENTS
        'total_clients': total_clients,

        # REVENUS
        'total_revenue': total_revenue,

        # CHART
        'months': months,
        'totals': totals,

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