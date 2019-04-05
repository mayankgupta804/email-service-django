from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone 
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from .forms import EmailForm
from .models import Email

def index(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = Email()
            email.email_id = form.cleaned_data['email_id']
            email.subject = form.cleaned_data['subject']
            email.body = form.cleaned_data['body']
            email.sent_at = timezone.now()
            email.save()
            messages.success(request, 'Email sent!')
            return HttpResponseRedirect(reverse('index') )

    else:    
        form = EmailForm()
    return render(request, 'email_sender/index.html', {
            'form': form
        })