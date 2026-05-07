from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required

from vehicles.models import Vehicle

from .models import Maintenance

from .forms import MaintenanceForm

@admin_required
def add_maintenance(request, pk):

    vehicle = get_object_or_404(
        Vehicle,
        id=pk
    )

    form = MaintenanceForm()

    if request.method == 'POST':

        form = MaintenanceForm(request.POST)

        if form.is_valid():

            maintenance = form.save(commit=False)

            maintenance.vehicle = vehicle

            maintenance.save()

            # 🚨 IMMOBILISER VEHICULE
            vehicle.statut = 'MAINTENANCE'

            vehicle.save()

            return redirect('vehicle_list')

    return render(
        request,
        'maintenance/add_maintenance.html',
        {
            'form': form,
            'vehicle': vehicle
        }
    )

@login_required
def maintenance_list(request):

    maintenances = Maintenance.objects.all()

    return render(
        request,
        'maintenance/maintenance_list.html',
        {
            'maintenances': maintenances
        }
    )

@admin_required
def close_maintenance(request, pk):

    maintenance = get_object_or_404(
        Maintenance,
        id=pk
    )

    maintenance.statut = 'TERMINEE'

    maintenance.save()

    # 🔓 REMETTRE VEHICULE DISPONIBLE
    vehicle = maintenance.vehicle

    vehicle.statut = 'DISPONIBLE'

    vehicle.save()

    return redirect('maintenance_list')

@admin_required
def close_maintenance(request, pk):

    maintenance = get_object_or_404(
        Maintenance,
        id=pk
    )

    maintenance.statut = 'TERMINEE'

    maintenance.save()

    # 🔓 REMETTRE VEHICULE DISPONIBLE
    vehicle = maintenance.vehicle

    vehicle.statut = 'DISPONIBLE'

    vehicle.save()

    return redirect('maintenance_list')