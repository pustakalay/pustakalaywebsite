from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse, JsonResponse

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
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, "contact/view.html", context)

