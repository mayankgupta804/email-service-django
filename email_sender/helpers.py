from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone 

from .models import Email

def save_emails(email_id_list, cc_list, bcc_list, subject, body):

    for email_id in email_id_list:
        email_id = email_id.strip()
        if len(email_id) > 0:
            error = save_email_data(email_id, subject, body)
            if error is not None:
                return error

    for cc in cc_list:
        cc = cc.strip()
        if len(cc) > 0:
            error = save_email_data(cc, subject, body)
            if error is not None:
                return error

    for bcc in bcc_list:
        bcc = bcc.strip()
        if len(bcc) > 0:
            error = save_email_data(bcc, subject, body)
            if error is not None:
                return error

def save_email_data(email_id, subject, body):
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