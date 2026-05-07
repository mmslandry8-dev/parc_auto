from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required

from rentals.models import Rental

from .models import Payment
from .forms import PaymentForm


@login_required
def create_payment(request, pk):

    """
    Effectuer paiement
    """

    rental = get_object_or_404(
        Rental,
        id=pk
    )

    form = PaymentForm()

    if request.method == 'POST':

        form = PaymentForm(request.POST)

        if form.is_valid():

            payment = form.save(commit=False)

            payment.rental = rental

            payment.montant = rental.prix_total

            payment.save()

            return redirect('my_payments')

    return render(
        request,
        'payments/create_payment.html',
        {
            'form': form,
            'rental': rental
        }
    )


@login_required
def my_payments(request):

    """
    Historique paiements utilisateur
    """

    payments = Payment.objects.filter(
        rental__client=request.user
    )

    return render(
        request,
        'payments/my_payments.html',
        {
            'payments': payments
        }
    )


@login_required
@admin_required
def validate_payment(request, pk):

    """
    Validation paiement
    """

    payment = Payment.objects.get(id=pk)

    payment.statut = 'PAYE'

    payment.save()

    return redirect('admin_dashboard')