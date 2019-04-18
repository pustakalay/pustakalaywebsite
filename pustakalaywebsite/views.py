from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings

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
        name = contact_form.cleaned_data.get('fullname')
        email = contact_form.cleaned_data.get('email')
        content = contact_form.cleaned_data.get('content')
        context = {
            'name': name,
            'content': content
        }
        txt_ = get_template("contact/contact-us.txt").render(context)
#         html_ = get_template("contact/contact-us.html").render(context)
        subject = 'Thank you for contacting Pustakalay'
        from_email = settings.DEFAULT_FROM_EMAIL
        bcc = [settings.DEFAULT_FROM_EMAIL]
        recipient_list = [email]
        email_message = EmailMessage(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    bcc
            )        
        email_message.send(fail_silently=False)        
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission."})
        else:
            messages.success(request, "Thank you for your submission.")

    if contact_form.errors:
        errors = contact_form.errors.as_json()        
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
        else:
            messages.error(request, contact_form.errors)
    return render(request, "contact/view.html", context)

