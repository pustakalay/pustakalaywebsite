from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, login
from .signals import user_logged_in
from django.contrib.auth.password_validation import validate_password
from sms.utils import verify_otp
import re

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserDetailChangeForm(forms.ModelForm):
    full_name = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    email  = forms.EmailField(widget=forms.EmailInput(attrs={"class": 'form-control'}))
    class Meta:
        model = User
        fields = ['full_name', 'email']

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'phone', 'email', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class LoginForm(forms.Form):
    phone    = forms.CharField(label='Phone')
    password = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        phone  = data.get("phone")
        password  = data.get("password")
        qs = User.objects.filter(phone=phone)
        if not qs.exists():
            raise forms.ValidationError("Mobile number not registered.")
        user = authenticate(request, username=phone, password=password)
        if user is None:
            raise forms.ValidationError("Invalid credentials")
        login(request, user)
        user_logged_in.send(user.__class__, instance=user, request=request)
        self.user = user
        return data

class SendOtpForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ('phone',)
        widgets = { 
            'phone': forms.TextInput(attrs={'id' : 'mobile-number'}),
        } 
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        phone_regex = re.compile(r'^\d{10}$')
        if not phone_regex.match(phone):
            raise forms.ValidationError("Invalid phone number.")
        return phone
    
class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    otp = forms.CharField(label='OTP', widget=forms.TextInput)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)
        widgets = { 
            'phone': forms.TextInput(attrs={'readonly': '', 'id' : 'from-mobile-number'}),
        } 
        
    def clean_otp(self):
        phone = self.cleaned_data.get("otp")
        phone_regex = re.compile(r'^\d{4}$')
        if not phone_regex.match(phone):
            raise forms.ValidationError("Otp must be 4 digit number.")
        data = verify_otp(self.cleaned_data.get("phone"), self.cleaned_data.get("otp"))
        if "success" != data['type']:
            raise forms.ValidationError("OTP not verified." + data['message'])
        return self.cleaned_data.get("otp")
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        phone_regex = re.compile(r'^\d{10}$')
        if not phone_regex.match(phone):
            raise forms.ValidationError("Invalid phone number.")
        return phone
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user