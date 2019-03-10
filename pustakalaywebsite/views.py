from django.shortcuts import render
from .forms import ContactForm

def home_page(request):
    context = {
        "title":"Pustakalay",
        "content":" Welcome to Pustakalay. Work in Progress.",
    }
    return render(request, "home_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Contact",
        "content":"Contact Page",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request, "contact/view.html", context)

