from django.http import HttpResponse

from django.shortcuts import get_object_or_404

from rentals.models import Rental

from sales.models import Sale

from .utils import html_to_pdf

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.shortcuts import redirect

@login_required
def invoice_rental(request, pk):

    rental = get_object_or_404(
        Rental,
        id=pk
    )

    # SECURITE
    if request.user != rental.client:

        if not request.user.groups.filter(
            name__in=['ADMIN', 'AGENT']
        ).exists():

            messages.error(
                request,
                "Accès refusé."
            )

            return redirect('home')

    # VERIFICATION PAIEMENT
    try:

        payment = rental.payment

        if payment.statut != 'PAYE':

            messages.error(
                request,
                "Paiement non validé."
            )

            return redirect('my_rentals')

    except:

        messages.error(
            request,
            "Aucun paiement trouvé."
        )

        return redirect('my_rentals')

    pdf = html_to_pdf(
        'invoices/invoice_rental.html',
        {
            'rental': rental,
            'payment': payment
        }
    )

    response = HttpResponse(
        pdf,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="facture_location_{pk}.pdf"'
    )

    return response

@login_required
def invoice_sale(request, pk):

    sale = get_object_or_404(
        Sale,
        id=pk
    )

    # SECURITE
    if request.user != sale.client:

        if not request.user.groups.filter(
            name__in=['ADMIN', 'AGENT']
        ).exists():

            messages.error(
                request,
                "Accès refusé."
            )

            return redirect('home')

    # VENTE PAYEE OBLIGATOIRE
    if sale.statut != 'PAYEE':

        messages.error(
            request,
            "Facture indisponible."
        )

        return redirect('my_sales')

    pdf = html_to_pdf(
        'invoices/invoice_sale.html',
        {
            'sale': sale
        }
    )

    response = HttpResponse(
        pdf,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="facture_vente_{pk}.pdf"'
    )

    return response