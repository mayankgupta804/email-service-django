from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from .forms import EmailForm
from .models import Email
from .helpers import save_emails

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