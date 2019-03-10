from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder" : "Your Full Name"}))    
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder" : "Your Email"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder" : "Your content"}))
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if ".com" not in email:
            raise ValidationError("Please enter valid email")
        return email