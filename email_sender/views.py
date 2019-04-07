from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

import csv
import os

from .forms import EmailForm
from .models import Email, CSVDocument
from .helpers import save_emails

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
            
def read_csv(filename):
    with open(filename, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        email_list = []
        for email in csv_reader:
            email_list.append(email)
        new_email_list = []    
        for i in range(len(email_list)):
            new_email_list.append(email_list[i][0])
        return new_email_list        