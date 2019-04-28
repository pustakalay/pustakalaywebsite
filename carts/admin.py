from django.contrib import admin

from .models import Cart, BookQuantity

class BookQuantityInline(admin.TabularInline):
    model = BookQuantity
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = (BookQuantityInline,)

admin.site.register(Cart, CartAdmin)
