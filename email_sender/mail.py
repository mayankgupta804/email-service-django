from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

import os

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
