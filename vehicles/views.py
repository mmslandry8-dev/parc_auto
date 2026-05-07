from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required

from .forms import VehicleForm


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