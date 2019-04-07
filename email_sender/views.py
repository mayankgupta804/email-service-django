from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

import os

from .forms import EmailForm
from .models import Email, CSVDocument
from .helpers import save_emails, read_csv, get_correct_email_ids
from .mail import send_email

def index(request):
    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            docfile = request.FILES.get('csv_file')
            if docfile is not None:
                csv_doc = CSVDocument(docfile=docfile)
                csv_doc.save()
            doc = CSVDocument.objects.first()
            csv_emails_list = []
            if doc is not None:
                file_path = os.path.join(settings.BASE_DIR + "/media", doc.docfile.path)
                csv_emails_list = read_csv(file_path)
                doc.delete()
            email_ids = form.cleaned_data['email_ids']
            email_id_list = email_ids.split(",")
            email_id_list = email_id_list + csv_emails_list
            cc = form.cleaned_data['cc']
            cc_list = cc.split(",")
            bcc = form.cleaned_data['bcc']
            bcc_list = bcc.split(",")
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            total_email_id_list = email_id_list + cc_list + bcc_list
            incorrect_email_id_list = save_emails(email_id_list, cc_list, bcc_list, subject, body)
            if len(total_email_id_list) == len(incorrect_email_id_list):
                messages.error(request, "ALL THE EMAIL IDS ARE INCORRECT!")
                return HttpResponseRedirect(reverse('index'))
            if len(incorrect_email_id_list) > 0:
                messages.error(request, "Emails could not be sent to these ids as these ids are incorrect: ")
                messages.error(request, [email for email in incorrect_email_id_list])
            correct_email_ids = get_correct_email_ids(total_email_id_list, incorrect_email_id_list)
            print(correct_email_ids)
            send_email.delay(email_id_list, cc_list, bcc_list, subject, body)
            messages.success(request, 'Email(s) sent!')
            return HttpResponseRedirect(reverse('index'))
    elif request.method == "GET":    
        form = EmailForm()
    return render(request, 'email_sender/index.html', {
            'form': form
        })    