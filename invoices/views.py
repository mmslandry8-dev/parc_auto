from django.http import HttpResponse

from django.shortcuts import get_object_or_404

from rentals.models import Rental

from sales.models import Sale

from .utils import html_to_pdf

def invoice_rental(request, pk):

    rental = get_object_or_404(
        Rental,
        id=pk
    )

    pdf = html_to_pdf(
        'invoices/invoice_rental.html',
        {
            'rental': rental
        }
    )

    response = HttpResponse(
        pdf,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = \
        f'attachment; filename="facture_location_{pk}.pdf"'

    return response

def invoice_sale(request, pk):

    sale = get_object_or_404(
        Sale,
        id=pk
    )

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

    response['Content-Disposition'] = \
        f'attachment; filename="facture_vente_{pk}.pdf"'

    return response