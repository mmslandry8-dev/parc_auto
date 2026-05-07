from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required

from .models import Customer

from rentals.models import Rental

from sales.models import Sale

@admin_required
def customer_detail(request, pk):

    customer = get_object_or_404(
        Customer,
        id=pk
    )

    rentals = Rental.objects.filter(
        client=customer.user
    )

    sales = Sale.objects.filter(
        client=customer.user
    )

    return render(
        request,
        'customers/detail.html',
        {
            'customer': customer,
            'rentals': rentals,
            'sales': sales
        }
    )

@admin_required
def customer_list(request):

    customers = Customer.objects.all()

    return render(
        request,
        'customers/list.html',
        {
            'customers': customers
        }
    )