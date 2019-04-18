from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

def home_page(request):
    context = {
        "title":"Pustakalay",
    }
    return render(request, "home_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Contact",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        messages.success(request, "Thank you for your submission.")
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission."})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        messages.error(request, contact_form.errors)
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, "contact/view.html", context)

