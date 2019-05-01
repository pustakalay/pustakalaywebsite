from .forms import LoginForm, RegisterForm, UserDetailChangeForm  
from django.views.generic import CreateView, FormView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pustakalaywebsite.mixins import NextUrlMixin, RequestFormAttachMixin
from django.contrib.auth import authenticate, login
from .signals import user_logged_in
from django.shortcuts import render, redirect 
from django.urls import reverse
from django.contrib import messages
from accounts.forms import SendOtpForm
from sms.utils import send_otp

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
    
    def get_initial(self):
        initial = super().get_initial()
        initial['phone'] = self.kwargs['phonenumber'] 
        return initial
    
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
    
def send_otp_view(request):
    form = SendOtpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():   
        phone_number = request.POST.get("phone") 
        data = send_otp(phone_number)
        if "success" == data['type']:
            request.session['otp-phone-number'] = phone_number    
            url = reverse('register_page', kwargs={'phonenumber':request.POST.get('phone')})  
            return redirect(url)
        else:
            messages.add_message(request, messages.ERROR, "Some Error occured while sending OTP.")
    return render(request, "accounts/send-otp.html", {'form' : form})
