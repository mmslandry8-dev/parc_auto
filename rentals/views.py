from datetime import timedelta

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from .models import Rental
from .forms import RentalForm

from vehicles.models import Vehicle
from accounts.decorators import admin_required


@login_required
def create_rental(request, pk):

    """
    Réserver un véhicule
    """

    vehicle = get_object_or_404(
        Vehicle,
        id=pk
    )

    form = RentalForm()

    if request.method == 'POST':

        form = RentalForm(request.POST)

        if form.is_valid():

            rental = form.save(commit=False)

            rental.client = request.user

            rental.vehicle = vehicle

            # CALCUL PRIX
            nb_jours = (
                rental.date_fin -
                rental.date_debut
            ).days

            rental.prix_total = (
                nb_jours *
                vehicle.prix_location
            )

            rental.save()

            return redirect('my_rentals')

    return render(
        request,
        'rentals/create_rental.html',
        {
            'form': form,
            'vehicle': vehicle
        }
    )

@login_required
def my_rentals(request):

    """
    Historique des locations
    """

    rentals = Rental.objects.filter(
        client=request.user
    )

    return render(
        request,
        'rentals/my_rentals.html',
        {
            'rentals': rentals
        }
    )

@login_required
@admin_required
def validate_rental(request, pk):

    """
    Valider réservation
    """

    rental = Rental.objects.get(id=pk)

    rental.statut = 'VALIDEE'

    rental.save()

    # VEHICULE LOUE
    rental.vehicle.statut = 'LOUE'

    rental.vehicle.save()

    return redirect('admin_dashboard')