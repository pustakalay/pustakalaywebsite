from django.shortcuts import render, redirect 
from .models import Cart, BookQuantity, BookRemovedQuantity
from booksapp.models import Book
from orders.models import Order
from accounts.forms import LoginForm
from addresses.forms import AddressCheckoutForm
from billing.models import BillingProfile
from addresses.models import Address
from django.http import JsonResponse
from django.contrib import messages

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
            "id": x.id,
            "url": x.get_absolute_url(),
            "name": x.name, 
            "price": x.price
            } 
            for x in cart_obj.books.all()]
    cart_data  = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_obj.save()
    if cart_obj.books_removed.count() != 0:
        for book in cart_obj.books_removed.all():
            book_removed_quantity = BookRemovedQuantity.objects.get(cart=cart_obj, book_removed=book)
            book_quantity = BookQuantity.objects.get(cart=cart_obj, book=book)
            messages.add_message(request, messages.ERROR, str(book_removed_quantity.quantity)+ " Book " + book.name + " has been removed from your cart. Because it went out of stock.")
            book_quantity.quantity = book_quantity.quantity -  book_removed_quantity.quantity
            book_quantity.save()
            book_removed_quantity.delete()
            if book_quantity.quantity <= 0:
                book_quantity.delete()
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    request.session['cart_item_count'] = cart_obj.get_books_count()
    return render(request, "carts/home.html", {'cart' : cart_obj})

def add_to_cart(request):
    book_id = request.POST.get('book_id')
    if book_id is not None:
        try:
            book_obj = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Book is out of stock.")
            return redirect("carts:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        book_quantity, created = BookQuantity.objects.get_or_create(cart=cart_obj, book=book_obj)
        if created:
            book_quantity.quantity = 1            
        else:
            book_quantity.quantity = book_quantity.quantity + 1
        book_quantity.save()
        request.session['cart_item_count'] = cart_obj.get_books_count()
        if request.is_ajax(): # Asynchronous JavaScript And XML / JSON
            json_data = {
                "book_id": book_obj.id,
                "quantity": book_quantity.quantity,
                "cartItemCount": cart_obj.get_books_count()
            }
            return JsonResponse(json_data)
    return redirect("carts:home")  

def remove_from_cart(request):
    book_id = request.POST.get('book_id')
    if book_id is not None:
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        book_obj = Book.objects.get(id=book_id)
        book_quantity, created = BookQuantity.objects.get_or_create(cart=cart_obj, book=book_obj)
        book_quantity.quantity = book_quantity.quantity - 1
        book_quantity.save()
        if book_quantity.quantity <= 0:
            book_quantity.delete()
        request.session['cart_item_count'] = cart_obj.books.count()
        if request.is_ajax(): # Asynchronous JavaScript And XML / JSON
            json_data = {
                "book_id": book_obj.id,
                "quantity": book_quantity.quantity,
                "cartItemCount": cart_obj.get_books_count()
            }
            return JsonResponse(json_data)
    return redirect("carts:home")      

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created or cart_obj.books.count() == 0:
        return redirect("carts:home")
    order_obj = None
    login_form = LoginForm(request=request)
    address_form = AddressCheckoutForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id) 
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
    
    if request.method == "POST":
        "check that order is done"
        cart_obj.save()
        if cart_obj.books_removed.count() != 0:
            for book in cart_obj.books_removed.all():
                messages.add_message(request, messages.ERROR, "Book " + book.name + " has been removed from your cart. Because it went out of stock.")
                cart_obj.books_removed.remove(book)
                request.session['cart_item_count'] = cart_obj.books.count()
                if cart_obj.books.count() == 0:
                    return redirect("carts:home")
                else:
                    return redirect("carts:checkout")
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            for book in order_obj.cart.books.all():
                book_quantity = BookQuantity.objects.get(cart=cart_obj, book=book)
                book.numberOfCopiesSold  += book_quantity.quantity
                book.inventory -= book_quantity.quantity
                book.save()
            del request.session['cart_item_count']
            del request.session['cart_id']
            cart_obj.active = False
            cart_obj.save()
            return redirect("carts:success")
    
    cart_obj.save()
    if cart_obj.books_removed.count() != 0:
        for book in cart_obj.books_removed.all():
            messages.add_message(request, messages.ERROR, "Book " + book.name + " has been removed from your cart. Because it went out of stock.")
            cart_obj.books_removed.remove(book)
            request.session['cart_item_count'] = cart_obj.books.count()
            if cart_obj.books.count() == 0:
                return redirect("carts:home")
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form, 
        "address_form": address_form,
        "address_qs": address_qs,
    }
    return render(request, "carts/checkout.html", context)

def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})
