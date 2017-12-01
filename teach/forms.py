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


class HomeworkForm(forms.Form):
    week_num = forms.IntegerField()
    homework = forms.FileField()
    deadline = forms.DateTimeField()
    mark = forms.IntegerField()
    statement = forms.CharField(max_length=800, required=False)


class SubmitForm(forms.Form):
    submit_id = forms.IntegerField()
    score = forms.IntegerField()
    remark = forms.CharField(max_length=800, required=False)


class AnnouncementForm(forms.Form):
    course = forms.CharField(max_length=20, required=True)
    title = forms.CharField(max_length=60, required=True)  # 标题
    content = forms.CharField(max_length=800,required=True)  # 内容
    post_time = forms.DateTimeField()  # 发布时间
