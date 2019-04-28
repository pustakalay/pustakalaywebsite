from django.conf.urls import url


from .views import (
        cart_home,          
        checkout_home,
        checkout_done_view,
        add_to_cart,
        remove_from_cart
        )

urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^checkout/success/$', checkout_done_view, name='success'),
    url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^add-to-cart/$', add_to_cart, name='add_to_cart'),
    url(r'^remove-from-cart/$', remove_from_cart, name='remove_from_cart'),
]
