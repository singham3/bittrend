from django import forms
from .models import Gallery


class GalleryForm(forms.Form):
    image = forms.FileField(required=True)

    class Meta:
        model = Gallery
        fields = ['image']

    def clean(self):
        cleaned_data = super(GalleryForm, self).clean()
        return cleaned_data
