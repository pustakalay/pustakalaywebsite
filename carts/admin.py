from django.contrib import admin

from .models import Cart, BookQuantity, BookRemovedQuantity

class BookQuantityInline(admin.TabularInline):
    model = BookQuantity
    extra = 1
    
class BookRemovedQuantityInline(admin.TabularInline):
    model = BookRemovedQuantity
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = (BookQuantityInline,BookRemovedQuantityInline,)

admin.site.register(Cart, CartAdmin)
