from datetime import timedelta

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User

from .models import Rental
from .forms import (
    RentalForm,
    AgentRentalForm
)

from vehicles.models import Vehicle

from accounts.decorators import (
    admin_required,
    agent_required,
    admin_or_agent_required
)

from payments.models import Payment

from django.contrib.auth.models import Group

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

            # =========================
            # VERIFICATION VEHICULE
            # =========================

            if vehicle.statut == 'VENDU':

                messages.error(
                    request,
                    "Ce véhicule est déjà vendu."
                )

                return redirect(
                    'vehicle_detail',
                    pk=vehicle.id
                )

            if vehicle.statut == 'MAINTENANCE':

                messages.error(
                    request,
                    "Ce véhicule est actuellement en maintenance."
                )

                return redirect(
                    'vehicle_detail',
                    pk=vehicle.id
                )

            # =========================
            # CONFLITS
            # =========================

            conflits = Rental.objects.filter(

                vehicle=vehicle,

                statut__in=[
                    'EN_ATTENTE',
                    'VALIDEE'
                ],

                date_debut__lte=rental.date_fin,

                date_fin__gte=rental.date_debut

            )

            if conflits.exists():

                messages.error(
                    request,
                    "Ce véhicule est déjà réservé pour ces dates."
                )

                return redirect(
                    'vehicle_detail',
                    pk=vehicle.id
                )

            # =========================
            # CALCUL PRIX
            # =========================

            nb_jours = (
                rental.date_fin -
                rental.date_debut
            ).days

            if nb_jours <= 0:

                nb_jours = 1

            rental.prix_total = (

                nb_jours *
                vehicle.prix_location

            )

            rental.save()

            messages.success(
                request,
                "Réservation effectuée avec succès."
            )

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
@login_required
@admin_or_agent_required
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

    messages.success(
        request,
        "Réservation validée."
    )

    return redirect('admin_dashboard')


# ==================================================
# LOCATION TERRAIN AGENT
# ==================================================

@login_required
@agent_required
def agent_create_rental(request):

    """
    Création location terrain par agent
    """

    form = AgentRentalForm()

    if request.method == 'POST':

        form = AgentRentalForm(request.POST)

        if form.is_valid():

            # CLIENT
            existing_client = form.cleaned_data[
                'existing_client'
            ]

            username = form.cleaned_data['username']

            email = form.cleaned_data['email']

            password = form.cleaned_data['password']

            # VEHICULE
            vehicle = form.cleaned_data['vehicle']

            # DATES
            date_debut = form.cleaned_data['date_debut']
            date_fin = form.cleaned_data['date_fin']

            # =========================
            # CREATION CLIENT
            # =========================

            # =========================
            # CLIENT EXISTANT
            # =========================

            if existing_client:

                user = existing_client

            # =========================
            # NOUVEAU CLIENT
            # =========================

            else:

                user, created = User.objects.get_or_create(

                    username=username,

                    defaults={
                        'email': email
                    }

                )

                if created:

                    user.set_password(password)

                    user.save()

                    # GROUPE CLIENT
                    client_group = Group.objects.get(
                        name='CLIENT'
                    )

                    user.groups.add(client_group)

            conflits = Rental.objects.filter(

                vehicle=vehicle,

                statut__in=[
                    'EN_ATTENTE',
                    'VALIDEE'
                ],

                date_debut__lte=date_fin,

                date_fin__gte=date_debut

            )

            if conflits.exists():

                messages.error(
                    request,
                    "Ce véhicule est déjà réservé pour ces dates."
                )

                return redirect(
                    'agent_create_rental'
                )   
            if vehicle.statut == 'VENDU':

                messages.error(
                    request,
                    "Ce véhicule est déjà vendu."
                )

                return redirect(
                    'agent_create_rental'
                )

            # =========================
            # CALCUL PRIX
            # =========================

            nb_jours = (
                date_fin -
                date_debut
            ).days

            if nb_jours <= 0:

                nb_jours = 1

            prix_total = (

                nb_jours *
                vehicle.prix_location

            )

            # =========================
            # CREATION LOCATION
            # =========================

            rental = Rental.objects.create(

                client=user,

                vehicle=vehicle,

                date_debut=date_debut,

                date_fin=date_fin,

                prix_total=prix_total,

                statut='VALIDEE'

            )

            # =========================
            # VEHICULE LOUE
            # =========================

            vehicle.statut = 'LOUE'

            vehicle.save()

            # =========================
            # PAIEMENT
            # =========================

            Payment.objects.create(

                rental=rental,

                montant=prix_total,

                methode='ESPECES',

                statut='PAYE'

            )

            messages.success(
                request,
                "Location terrain enregistrée avec succès."
            )

            return redirect(
                'agent_dashboard'
            )

    return render(
        request,
        'rentals/agent_create_rental.html',
        {
            'form': form
        }
    )