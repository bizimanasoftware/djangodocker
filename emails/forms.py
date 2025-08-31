# emails/forms.py

from django import forms

class EmailComposerForm(forms.Form):
    recipients = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'vTextField', 'size': '80'}),
        help_text="Comma-separated email addresses."
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'vTextField', 'size': '80'})
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 20, 'cols': 100})
    )
    attachments = forms.FileField(
        widget=forms.ClearableFileInput,
        required=False,
        help_text="You can upload one file."
    )
