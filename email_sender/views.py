from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone 
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


from .forms import EmailForm
from .models import Email

def index(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email_ids = form.cleaned_data['email_ids']
            email_id_list = email_ids.split(",")
            cc = form.cleaned_data['cc']
            cc_list = cc.split(",")
            bcc = form.cleaned_data['bcc']
            bcc_list = bcc.split(",")
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            error = save_emails(email_id_list, cc_list, bcc_list, subject, body)
            if error is not None:
                messages.error(request, error)
                return HttpResponseRedirect(reverse('index') )
            messages.success(request, 'Email sent!')
            return HttpResponseRedirect(reverse('index') )

    elif request.method == "GET":    
        form = EmailForm()
    return render(request, 'email_sender/index.html', {
            'form': form
        })

def save_emails(email_id_list, cc_list, bcc_list, subject, body):
    for email_id in email_id_list:
        print(email_id)
        error = save_data(email_id, subject, body)
        if error is not None:
            return error

    for cc in cc_list:
        error = save_data(cc, subject, body)
        if error is not None:
            return error

    for bcc in bcc_list:
        error = save_data(bcc, subject, body)
        if error is not None:
            return error

def save_data(email_id, subject, body):
    email = Email()
    try:
        validate_email(email_id)
    except ValidationError as e:
        print("Exception: {}".format(e))
        return "Incorrect email id: {}".format(email_id)

    email.email_id = email_id
    email.subject = subject
    email.body = body
    email.sent_at = timezone.now()
    email.save()

    return None