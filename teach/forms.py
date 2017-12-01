from django import forms
from django.forms import ModelForm
from .models import *

class PlanForm(forms.Form):
    week_num = forms.IntegerField()
    date = forms.DateField()
    topic = forms.CharField(max_length=200, required=False)

class ClasswareForm(forms.Form):
    week_num = forms.IntegerField()
    classware = forms.FileField()

class SubmitForm(forms.Form):
    submit_id = forms.IntegerField()
    score = forms.IntegerField()
    remark = forms.CharField(max_length=800, required=False)
