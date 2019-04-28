from django import template
from carts.models import BookQuantity
register = template.Library()

@register.inclusion_tag('booksapp/snippets/book_quantity.html')
def get_book_cart_quantity(book_obj, cart_obj):
    try:
        book_quantity = BookQuantity.objects.get(cart=cart_obj, book=book_obj)
        quantity = book_quantity.quantity
    except:
        quantity = 0
    return {'quantity': quantity,
            'book_id' : book_obj.id
            }