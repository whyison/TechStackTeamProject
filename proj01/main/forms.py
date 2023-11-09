from django import forms
from .models import Location

class SearchForm(forms.Form):
    job_position = forms.CharField(max_length=50, required=True)
    location_sido = forms.ModelChoiceField(queryset=Location.objects.filter(parent=None), empty_label='시/도 선택', required=False)
    location_sigg = forms.ModelChoiceField(queryset=Location.objects.none(), empty_label='시/군구 선택', required=False)
