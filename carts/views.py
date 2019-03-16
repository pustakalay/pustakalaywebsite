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
    
    login_form = LoginForm()
    guest_form = GuestForm()
    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form, 
        "guest_form": guest_form
    }
    return render(request, "carts/checkout.html", context)
