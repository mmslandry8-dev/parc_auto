from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required

from vehicles.models import Vehicle

from .models import Sale

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

@admin_required
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