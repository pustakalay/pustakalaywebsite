from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from addresses.models import Address
from billing.models import BillingProfile
from .forms import AddressCheckoutForm, AddressForm
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from carts.models import Cart
from orders.models import Order

class AddressListView(LoginRequiredMixin, ListView):
    template_name = 'addresses/list.html'

    def get_queryset(self):
        request = self.request
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        return Address.objects.filter(billing_profile=billing_profile)

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AddressForm
    success_url = '/addresses'
    template_name = 'addresses/update.html'

    def get_queryset(self):
        request = self.request
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        return Address.objects.filter(billing_profile=billing_profile)

class AddressCreateView(LoginRequiredMixin, CreateView):
    template_name = 'addresses/update.html'
    form_class = AddressForm
    success_url = '/addresses'

    def form_valid(self, form):
        request = self.request
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        instance = form.save(commit=False)
        instance.billing_profile = billing_profile
        instance.save()
        return super(AddressCreateView, self).form_valid(form)
    
def checkout_address_create_view(request):
    form = AddressCheckoutForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.save()
            request.session["shipping_address_id"] = instance.id
        else:
            print("Error here")
            return redirect("carts:checkout")
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect("carts:checkout") 


def checkout_address_reuse_view(request):
    if request.user.is_authenticated():
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method == "POST":
            shipping_address = request.POST.get('shipping_address', None)
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session["shipping_address_id"] = shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect("carts:checkout") 

def change_address(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            cart_obj, cart_created = Cart.objects.new_or_get(request)
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
            order_obj.shipping_address = None
            order_obj.save()
    return redirect("carts:checkout")