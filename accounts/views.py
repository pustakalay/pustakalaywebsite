from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import LoginForm, RegisterForm, GuestForm   
from django.utils.http import is_safe_url
from .models import GuestEmail
from django.views.generic import CreateView, FormView

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
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
        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'
    
# def login_page(request):
#     login_form = LoginForm(request.POST or None)
#     context = {'form' : login_form}
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if login_form.is_valid():
#         username = login_form.cleaned_data.get('username')
#         password = login_form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect('home')
#         else:
#             context['error'] = "Incorrect Password"
#     return render(request, 'accounts/login.html', context)
# 
# 
# User = get_user_model()
# 
# 
# def register_page(request):
#     register_form = RegisterForm(request.POST or None)
#     context = {'form' : register_form}
#     if register_form.is_valid():
#         username = register_form.cleaned_data.get('username')
#         email = register_form.cleaned_data.get('email')
#         password = register_form.cleaned_data.get('password')
#         user = User.objects.create_user(username, email, password)
#         return redirect('home')
#     return render(request, 'accounts/register.html', context)


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