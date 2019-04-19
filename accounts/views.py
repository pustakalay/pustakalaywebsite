from django.shortcuts import redirect
from .forms import LoginForm, RegisterForm, UserDetailChangeForm  
from django.views.generic import CreateView, FormView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from pustakalaywebsite.mixins import NextUrlMixin, RequestFormAttachMixin
from django.contrib.auth import authenticate, login
from .signals import user_logged_in

class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    def get_object(self):
        return self.request.user

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/account/details/'
    
    def form_valid(self, form):
        form.save()
        phone = self.request.POST['phone']
        password = self.request.POST['password1']
        user = authenticate(username=phone, password=password)
        login(self.request, user)
        user_logged_in.send(user.__class__, instance=user, request=self.request)
        return redirect(self.success_url)
    
class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Your Account Details'
        return context

    def get_success_url(self):
        return reverse("account:home")