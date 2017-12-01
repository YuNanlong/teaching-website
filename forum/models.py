# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from teach.models import Course

# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=25)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Post(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, null= True,on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    content = models.CharField(max_length=1000, default='')
    is_top = models.IntegerField(default=0)
    is_best = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    layer_number = models.IntegerField(default=0)
    files = models.FileField(upload_to='files/')


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=256, default='')
    time = models.DateTimeField(auto_now_add=True)
