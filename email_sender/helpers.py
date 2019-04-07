from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone 

import csv

from .models import Email

def save_emails(email_id_list, cc_list, bcc_list, subject, body):
    incorrect_email_id_list = []
    for email_id in email_id_list:
        email_id = email_id.strip()
        if len(email_id) > 0:
            cc = False
            bcc = False
            error_email_id = save_email_data(email_id, subject, body, cc, bcc)
            if error_email_id:
                incorrect_email_id_list.append(email_id)

    for cc_email in cc_list:
        cc_email = cc_email.strip()
        if len(cc_email) > 0:
            cc = True
            bcc = False
            error_email_id = save_email_data(cc_email, subject, body, cc, bcc)
            if error_email_id:
                incorrect_email_id_list.append(cc_email)

    for bcc_email in bcc_list:
        bcc_email = bcc_email.strip()
        if len(bcc_email) > 0:
            cc = False
            bcc = True
            error_email_id = save_email_data(bcc_email, subject, body, cc, bcc)
            if error_email_id:
                incorrect_email_id_list.append(bcc_email)
                
    return incorrect_email_id_list        

def save_email_data(email_id, subject, body, cc, bcc):
    email = Email()
    try:
        validate_email(email_id)
    except ValidationError as e:
        print("Exception: {}".format(e))
        print("Invalid email address: {}".format(email_id))
        return True

    email.email_id = email_id
    email.cc = cc
    email.bcc = bcc
    email.subject = subject
    email.body = body
    email.sent_at = timezone.now()
    email.save()

    return False

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