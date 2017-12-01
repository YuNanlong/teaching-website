from django.contrib import admin
from .models import *

admin.site.register([Course, Plan, Video, Classware, Homework, Notice, Submit])
