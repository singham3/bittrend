from django import forms
from .models import Logs


class LogsForm(forms.Form):
    message = forms.CharField(required=True, widget=forms.Textarea)
    device_name = forms.CharField(required=False)
    ip_address = forms.CharField(required=False)

    class Meta:
        model = Logs
        fields = ['message', 'device_name', 'ip_address']

    def clean(self):
        cleaned_data = super(LogsForm, self).clean()
        return cleaned_data
