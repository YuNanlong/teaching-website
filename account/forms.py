from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm

class TeacherEditForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=20)
    desc_achive = forms.CharField(max_length=100, required=False)
    desc_teach_type = forms.CharField(max_length=100, required=False)
    desc_publish = forms.CharField(max_length=100, required=False)
    desc_honor = forms.CharField(max_length=100, required=False)
    desc_more = forms.CharField(max_length=100, required=False)

class StudentEditForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=20)
