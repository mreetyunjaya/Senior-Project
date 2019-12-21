from .models import Remedy
from django import forms


class RemedyForm(forms.ModelForm):

    class Meta:
        model = Remedy
        fields = ["remediation", "status", "patches"]
