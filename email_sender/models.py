from django.db import models

class Email(models.Model):
    email_id = models.EmailField()
    subject = models.CharField(max_length=20)
    body = models.TextField(max_length=1000)
    sent_at = models.DateTimeField()

class CSVDocument(models.Model):
    docfile = models.FileField(upload_to='documents')