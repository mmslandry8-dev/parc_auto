from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.decorators import (
    admin_required,
    admin_or_agent_required
)

from .forms import VehicleForm

from .models import Vehicle
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

@login_required
@admin_or_agent_required
def add_vehicle(request):

    """
    Ajouter un véhicule
    """

    form = VehicleForm()

    if request.method == 'POST':

        form = VehicleForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('vehicle_list')

    return render(
        request,
        'vehicles/add_vehicle.html',
        {
            'form': form
        }
    )

@login_required
def vehicle_list(request):

    """
    Liste intelligente des véhicules
    """

    vehicles = Vehicle.objects.all()

    # =========================
    # RECHERCHE
    # =========================

    search = request.GET.get('search')

    if search:

        vehicles = vehicles.filter(

            modele__icontains=search

        ) | vehicles.filter(

            marque__icontains=search

        )

    # =========================
    # FILTRE TYPE
    # =========================

    vehicle_type = request.GET.get('type')

    if vehicle_type:

        vehicles = vehicles.filter(
            type=vehicle_type
        )

    # =========================
    # FILTRE STATUT
    # =========================

    statut = request.GET.get('statut')

    if statut:

        vehicles = vehicles.filter(
            statut=statut
        )

    # =========================
    # PAGINATION
    # =========================
    vehicles = Vehicle.objects.all().order_by('-id')

    paginator = Paginator(
        vehicles,
        6
    )

    page_number = request.GET.get('page')

    vehicles = paginator.get_page(
        page_number
    )

    context = {

        'vehicles': vehicles

    }

    return render(
        request,
        'vehicles/vehicle_list.html',
        context
    )

def vehicle_detail(request, pk):
    """
    Détails d'un véhicule
    """

    vehicle = Vehicle.objects.get(id=pk)

    return render(
        request,
        'vehicles/vehicle_detail.html',
        {
            'vehicle': vehicle
        }
    )

@login_required
@admin_or_agent_required
def delete_vehicle(request, pk):
    """
    Supprimer un véhicule
    """

    vehicle = Vehicle.objects.get(id=pk)

    vehicle.delete()

    return redirect('vehicle_list')

@login_required
@admin_or_agent_required
def update_vehicle(request, pk):
    """
    Modifier un véhicule
    """

    vehicle = Vehicle.objects.get(id=pk)

    form = VehicleForm(instance=vehicle)

    if request.method == 'POST':

        form = VehicleForm(
            request.POST,
            request.FILES,
            instance=vehicle
        )

        if form.is_valid():

            form.save()

            return redirect('vehicle_list')

    return render(
        request,
        'vehicles/update_vehicle.html',
        {
            'form': form,
            'vehicle': vehicle
        }
    )