from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm

class TeacherEditForm(forms.Form):
    username = forms.CharField(max_length=150, label="用户名")
    email = forms.EmailField(required=False, label="电子邮箱")
    phone = forms.CharField(max_length=20, label="电话号码")
    desc_achive = forms.CharField(max_length=100, required=False, label="教学成果")
    desc_teach_type = forms.CharField(max_length=100, required=False, label="教学风格")
    desc_publish = forms.CharField(max_length=100, required=False, label="出版作品")
    desc_honor = forms.CharField(max_length=100, required=False, label="所获荣誉")
    desc_more = forms.CharField(max_length=100, required=False, label="更多信息")

class StudentEditForm(forms.Form):
    username = forms.CharField(max_length=150, label="用户名")
    email = forms.EmailField(required=False, label="电子邮箱")
    phone = forms.CharField(max_length=20, label="电话号码")
