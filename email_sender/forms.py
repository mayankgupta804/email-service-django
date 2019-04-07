from django import forms

class EmailForm(forms.Form):
    email_ids = forms.CharField(max_length=500, label="Email(s)")
    cc = forms.CharField(max_length=500, label="cc", required=False)
    bcc = forms.CharField(max_length=500, label="bcc", required=False)
    subject = forms.CharField(max_length=500, label="Subject")
    body = forms.CharField(label="Body",widget=forms.Textarea(
                        attrs={'placeholder': 'Enter your message here'}))    
