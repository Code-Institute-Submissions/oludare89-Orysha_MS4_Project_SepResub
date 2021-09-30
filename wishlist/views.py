from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import Product
from wishlist.contexts import wishlist_contents

# Create your views here.


def show_wishlist(request):
    """ A view to show the wishlist """

    return render(request, 'wishlist/wishlist.html')


@login_required
def add_to_wishlist(request, item_id):
    """ Add a quantity of the specified product to the wishlist """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
        wishlist = request.session.get('wishlist', {})

    if size:
        if item_id in list(wishlist.keys()):
            if size in wishlist[item_id]['items_by_size'].keys():
                wishlist[item_id]['items_by_size'][size] += quantity
                messages.success(request, f"Updated size {size.upper()}
                                 {product.name} quantity to {wishlist[item_id]
                                 ['items_by_size'][size]}")
            else:
                wishlist[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()}
                                 {product.name} to your wishlist')
        else:
            wishlist[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()}
                             {product.name} to your wishlist')
    else:
        if item_id in list(wishlist.keys()):
            wishlist[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to
                             {wishlist[item_id]}')
        else:
            wishlist[item_id] = quantity
            messages.success(request, f'Added {product.name} to your cart')

    in_wishlist = True
    request.session['wishlist'] = wishlist
    return redirect(redirect_url)


@login_required
def adjust_wishlist(request, item_id):
    """Adjust the quantity of the specified product by the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    wishlist = request.session.get('wishlist', {})

    if size:
        if quantity > 0:
            wishlist[item_id]['items_by_size'][size] = quantity
            messages.success(request, f"Updated size {size.upper()}
                             {product.name} quantity to {wishlist[item_id]
                             ['items_by_size'][size]}")
        else:
            del wishlist[item_id]['items_by_size'][size]
            if not wishlist[item_id]['items_by_size']:
                wishlist.pop(item_id)
            messages.success(request, f'Removed size {size.upper()}
                             {product.name} from your wishlist')
    else:
        if quantity > 0:
            wishlist[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to
                             {wishlist[item_id]}')
        else:
            wishlist.pop(item_id)
            messages.success(request, f'Removed {product.name}
                             from your wishlist')

    request.session['wishlist'] = wishlist
    return redirect(reverse('show_wishlist'))


@login_required
def remove_from_wishlist(request, item_id):
    """ Remove the specified product from the wishlist """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        wishlist = request.session.get('wishlist', {})

        if size:
            del wishlist[item_id]['items_by_size'][size]
            if not wishlist[item_id]['items_by_size']:
                wishlist.pop(item_id)
            messages.success(request, f'Removed size {size.upper()}
                             {product.name} from your wishlist')
        else:
            wishlist.pop(item_id)
            messages.success(request, f'Removed {product.name}
                             from your wishlist')

        in_wishlist = False
        request.session['wishlist'] = wishlist
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
