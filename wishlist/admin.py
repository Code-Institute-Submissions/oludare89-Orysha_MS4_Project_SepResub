from django.contrib import admin
from .models import Wishlist, WishlistLineItem


class WishlistLineItemAdminInline(admin.TabularInline):
    model = WishlistLineItem
    readonly_fields = ('wishlist_id', 'product',)


class WishlistAdmin(admin.ModelAdmin):
    inlines = (WishlistLineItemAdminInline,)

    readonly_fields = ('wishlist_id', 'date',
                       'user_profile',)

    fields = ('wishlist_id', 'user_profile', 'date',)

    list_display = ('wishlist_id', 'date',)

    ordering = ('-date',)

admin.site.register(Wishlist, WishlistAdmin)
