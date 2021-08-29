from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm
from wishlist.contexts import wishlist_contents

# Create your views here.

def show_wishlist(request):
    """ A view to show the wishlist """
    
    return render(request, 'wishlist/wishlist.html', context)


@login_required
def add_product(request):
    """ A view to add products to the site """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only the site owner can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ To edit an existing product on the site """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only the site owner can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated product!")
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, "Failed to update product. Please ensure form is valid.")
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_wishlist_item(request, product_id):
    """ To delete an existing wishlist item """
    
        
    product = get_object_or_404(Product, pk=product_id)
    wishlist_item.delete()
    messages.success(request, 'Wishlist item deleted!')
    return redirect(reverse('wishlist'))
