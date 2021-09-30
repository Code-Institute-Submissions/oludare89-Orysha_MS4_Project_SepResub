import uuid

from django.db import models

from products.models import Product
from profiles.models import UserProfile


class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='wishlists')
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def _generate_wishlist_id(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.wishlist_id:
            self.wishlist_id = self._generate_wishlist_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.wishlist_id


class WishlistLineItem(models.Model):
    wishlist_id = models.ForeignKey(Wishlist, null=False, blank=False,
                                    on_delete=models.CASCADE,
                                    related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)

    def __str__(self):
        return f'SKU {self.product.sku} on wishlist{self.wishlist.wishlist_id}'
