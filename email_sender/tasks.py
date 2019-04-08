from celery import shared_task, task
from datetime import date
from django.core.mail import EmailMessage, mail_admins
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import os

from .models import Email

@shared_task
def send_email(email_id_list, cc_list, bcc_list, subject, body):
    email = EmailMessage(
    subject,
    body,
    settings.EMAIL_HOST_USER,
    email_id_list,
    bcc_list,
    cc=cc_list,
    )

    email.send(fail_silently=False)

@task
def send_stats():
    today = date.today()
    emails_today =  Email.objects.filter(sent_at__year=today.year,sent_at__month=today.month,sent_at__day=today.day)
    subject = "Stats for the date: {}".format(str(today))
    html_message = render_to_string('email_sender/email_statistics.html', {'total_emails': len(emails_today), 'mails': emails_today})
    plain_message = strip_tags(html_message)
    mail_admins(subject, plain_message, fail_silently=False, connection=None, html_message=None)
