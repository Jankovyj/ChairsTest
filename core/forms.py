from django import forms
from core.models import Lease

class CheckAvailabilityForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()


class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['amount']
