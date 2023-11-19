from django import forms
from BackBridge.models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'photo')