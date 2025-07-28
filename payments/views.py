from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from . import forms
from item.models import Item
import uuid
from .utils.mercadopago import MercadoData

# Create your views here.

def orderView(request, pk):
    item = get_object_or_404(Item, id=pk)
    if request.method == 'POST':
        form = forms.OrderForm(request.POST, item=item)

        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            order.item = item
            order.save()

            return redirect('payments:shipping', pk=order.pk)

    else:
        form = forms.OrderForm()

    return render(request, 'payments/order.html', {
        'form': form,
        'item': item,
        'title': 'Orden'
    })

def shippingView(request, pk):
    order = get_object_or_404(models.Order, id=pk)
    if request.method == "POST":
        form = forms.ShippingForm(request.POST) # type: ignore

        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.order = order
            shipping.save()

            return redirect('payments:checkout', pk=order.pk)

    else:
        form = forms.ShippingForm()

    return render(request, 'payments/shipping.html', {
        'form': form,
        'order': order,
        'title': 'Shipping'
    })


def paymentsView(request, pk):
    order = get_object_or_404(models.Order, id=pk)
    if request.method == 'POST':
        form = forms.PaymentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            payment = form.save(commit=False)
            payment_data = {
            # Datos de la Compra
            "total": float(order.total),   # type: ignore
            "payment_method_id": data['payment_method'],  
            "email": request.user.email,  

            # Datos de la tarjeta
            "card_number": data['card_num'],  
            "security_code": data['security_code'],             
            "expiration_month": int(data['expiration_month']),             
            "expiration_year": int(data['expiration_year']),            
            "name": 'APRO',   

            # Cuotas
            "installments": 1,  # Número de cuotas (opcional, por defecto 1)

            # Clave única para evitar pagos duplicados (idealmente un UUID)
            "unique_value": str(uuid.uuid4())
}
            print("Creando MercadoData...")  # Debug
            mercado = MercadoData(**payment_data) # type: ignore


            print("Obteniendo data to save...")  # Debug
            data_to_save = mercado.get_data_to_save()
            print("Data to save:", data_to_save)  # Debug

            payment.order = order
            payment.amount = order.total
            payment.external_payment_id = data_to_save['external_payment_id']
            payment.status = data_to_save['status']
            payment.provider_data = data_to_save['provider_data']
            payment.paid_at = data_to_save['paid_at']
            
            print("Guardando payment...")  # Debug
            payment.save()
            print("Payment guardado exitosamente!")  # Debug

            return redirect('payments:success', pk=payment.pk)
    
    else:
        form = forms.PaymentForm()

    return render(request, 'payments/checkout.html', {
        'form': form,
        'order': order,
        'title': 'Checkout'
    })


def successView(request, pk):
    payment = get_object_or_404(models.Payment, id=pk)
    if payment.status == "approved":
        return render(request, 'payments/success.html')
    else:
        raise ValueError('Something went wrong')