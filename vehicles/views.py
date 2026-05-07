from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required

from .forms import VehicleForm

from .models import Vehicle
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required


@login_required
@admin_required
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
    Liste des véhicules
    visible par tous les utilisateurs connectés
    """

    vehicles = Vehicle.objects.all()

    return render(
        request,
        'vehicles/vehicle_list.html',
        {
            'vehicles': vehicles
        }
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

@admin_required
def delete_vehicle(request, pk):
    """
    Supprimer un véhicule
    """

    vehicle = Vehicle.objects.get(id=pk)

    vehicle.delete()

    return redirect('vehicle_list')

@admin_required
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