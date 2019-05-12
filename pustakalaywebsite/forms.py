from django import forms
from django.core.exceptions import ValidationError
import re   

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder" : "Your Full Name"}))    
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder" : "Your Email"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder" : "Your content"}))
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if ".com" not in email:
            raise ValidationError("Please enter valid email")
        return email
    
class PinCodeForm(forms.Form):
    pincode = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder" : "Enter Pincode"}))    
    
    def clean_pincode(self):
        pincode = self.cleaned_data.get("pincode")
        pincode_regex = re.compile(r'^\d{6}$')
        if not pincode_regex.match(pincode):
            raise forms.ValidationError("Invalid PinCode.")
        return pincode