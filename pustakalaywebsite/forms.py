from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder" : "Your Full Name"}))    
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder" : "Your Email"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder" : "Your content"}))
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if ".com" not in email:
            raise ValidationError("Please enter valid email")
        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    
class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password' , widget=forms.PasswordInput)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is already taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already taken.")
        return email
    
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords must match")
        return self.cleaned_data
        
        
