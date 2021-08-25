from django.shortcuts import render, reverse, redirect
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment.")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JSPEYFaQkZ2A05K8zAMetHu3DXdFVOla4Ozc2Rxpkwcltub9m64qbSqyro4wjQTyrL6kF1YCBN7HGFHd6BIyWJC00E4x1ZADF',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
