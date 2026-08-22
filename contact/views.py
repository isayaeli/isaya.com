from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render

from .forms import ContactForm


def home(request):
    submitted = False
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            email = EmailMessage(
                subject=f"New contact message from {contact_message.name}",
                body=contact_message.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_RECIPIENT],
                reply_to=[contact_message.email],
            )
            email.send(fail_silently=True)
            form = ContactForm()
            submitted = True

    return render(request, "index.html", {"form": form, "submitted": submitted})
