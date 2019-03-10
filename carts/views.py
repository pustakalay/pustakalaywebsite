from django.shortcuts import render, redirect 
from .models import Cart
from booksapp.models import Book
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail 
from billing.models import BillingProfile

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {'cart' : cart_obj})

def cart_update(request):
    book_id = request.POST.get('book_id')
    if book_id is not None:
        try:
            book_obj = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            print("Show message to user, Book is gone?")
            return redirect("carts:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if book_obj in cart_obj.books.all():
            cart_obj.books.remove(book_obj)
        else:
            cart_obj.books.add(book_obj)
        request.session['cart_item_count'] = cart_obj.books.count()
    return redirect("carts:home")

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.books.count() == 0:
        return redirect("cart:home")
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated():
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(
                                        email=guest_email_obj.email)
    else:
        pass
    
    if billing_profile is not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form, 
        "guest_form": guest_form
    }
    return render(request, "carts/checkout.html", context)
