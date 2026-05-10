from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required, admin_or_agent_required

from vehicles.models import Vehicle

from .models import Sale

from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password

from payments.models import Payment

from accounts.utils import assign_user_role

from accounts.decorators import agent_required

from .forms import AgentSaleForm

@login_required
def request_sale(request, pk):

    vehicle = get_object_or_404(
        Vehicle,
        id=pk
    )

    # 🚨 véhicule déjà vendu
    if vehicle.statut == 'VENDU':

        return redirect('vehicle_list')

    Sale.objects.create(

        vehicle=vehicle,

        client=request.user,

        prix_vente=vehicle.prix_vente

    )

    return redirect('my_sales')

@login_required
def my_sales(request):

    sales = Sale.objects.filter(
        client=request.user
    )

    return render(
        request,
        'sales/my_sales.html',
        {
            'sales': sales
        }
    )

@admin_required
def sales_list(request):

    sales = Sale.objects.all()

    return render(
        request,
        'sales/sales_list.html',
        {
            'sales': sales
        }
    )

@login_required
@admin_or_agent_required
def validate_sale(request, pk):

    sale = get_object_or_404(
        Sale,
        id=pk
    )

    sale.statut = 'VALIDEE'

    sale.save()

    # 🚗 MARQUER VEHICULE VENDU
    vehicle = sale.vehicle

    vehicle.statut = 'VENDU'

    vehicle.save()

    return redirect('sales_list')

@admin_required
def pay_sale(request, pk):

    sale = get_object_or_404(
        Sale,
        id=pk
    )

    sale.statut = 'PAYEE'

    sale.save()

    return redirect('sales_list')

@login_required
@agent_required
def agent_create_sale(request):

    """
    Vente terrain par agent
    """

    form = AgentSaleForm()

    if request.method == 'POST':

        form = AgentSaleForm(request.POST)

        if form.is_valid():

            # =========================
            # CLIENT
            # =========================

            username = form.cleaned_data['username']

            email = form.cleaned_data['email']

            password = form.cleaned_data['password']

            # EXISTE ?
            user_exists = User.objects.filter(
                username=username
            ).exists()

            if user_exists:

                messages.error(
                    request,
                    "Ce nom utilisateur existe déjà."
                )

                return redirect(
                    'agent_create_sale'
                )

            # CREATION CLIENT
            user = User.objects.create(

                username=username,

                email=email,

                password=make_password(password)

            )

            # ROLE CLIENT
            assign_user_role(
                user,
                'CLIENT'
            )

            # =========================
            # VEHICULE
            # =========================

            vehicle = form.cleaned_data['vehicle']

            # SECURITE
            if vehicle.statut != 'DISPONIBLE':

                messages.error(
                    request,
                    "Véhicule indisponible."
                )

                return redirect(
                    'agent_create_sale'
                )

            # =========================
            # CREATION VENTE
            # =========================

            sale = Sale.objects.create(

                vehicle=vehicle,

                client=user,

                prix_vente=vehicle.prix_vente,

                statut='PAYEE'

            )

            # =========================
            # PAIEMENT
            # =========================

            Payment.objects.create(

                rental=None,

                montant=vehicle.prix_vente,

                methode=form.cleaned_data['methode'],

                statut='PAYE'

            )

            # =========================
            # VEHICULE VENDU
            # =========================

            vehicle.statut = 'VENDU'

            vehicle.save()

            messages.success(
                request,
                "Vente enregistrée avec succès."
            )

            return redirect(
                'agent_dashboard'
            )

    return render(

        request,

        'sales/agent_create_sale.html',

        {
            'form': form
        }

    )

from django.contrib import messages

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.contrib.auth.decorators import login_required

from accounts.decorators import (
    admin_or_agent_required
)

from .models import Sale

@login_required
@admin_or_agent_required
def validate_sale(request, pk):

    """
    Validation vente
    """

    sale = get_object_or_404(
        Sale,
        id=pk
    )

    sale.statut = 'VALIDEE'
    sale.save()

    # VEHICULE VENDU
    sale.vehicle.statut = 'VENDU'
    sale.vehicle.save()

    messages.success(
        request,
        "Vente validée avec succès."
    )

    return redirect('operations_management')

@login_required
@admin_or_agent_required
def refuse_sale(request, pk):

    """
    Refus vente
    """

    sale = get_object_or_404(
        Sale,
        id=pk
    )

    sale.statut = 'REFUSEE'
    sale.save()

    messages.warning(
        request,
        "Vente refusée."
    )

    return redirect('operations_management')

@login_required
@admin_or_agent_required
def cancel_sale(request, pk):

    """
    Annulation vente
    """

    sale = get_object_or_404(
        Sale,
        id=pk
    )

    # VENTE ANNULEE
    sale.statut = 'REFUSEE'
    sale.save()

    # VEHICULE DISPONIBLE
    sale.vehicle.statut = 'DISPONIBLE'
    sale.vehicle.save()

    messages.warning(
        request,
        "Vente annulée."
    )

    return redirect('operations_management')