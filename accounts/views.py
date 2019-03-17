from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, GuestForm   
from django.utils.http import is_safe_url
from .models import GuestEmail

def login_page(request):
    login_form = LoginForm(request.POST or None)
    context = {'form' : login_form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('home')
        else:
            context['error'] = "Incorrect Password"
    return render(request, 'accounts/login.html', context)


User = get_user_model()


def register_page(request):
    register_form = RegisterForm(request.POST or None)
    context = {'form' : register_form}
    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')
        user = User.objects.create_user(username, email, password)
        return redirect('home')
    return render(request, 'accounts/register.html', context)


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email       = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")