from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

Gender_Choice = (
    ('M', '男'),
    ('F', '女'),
)
'''
    以下为Django自带User中的字段，可以直接引用

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
'''


class Teacher(models.Model):
    teacher = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=Gender_Choice)
    college = models.CharField(max_length=30)
    department = models.CharField(max_length=30, blank=True)
    position = models.CharField(max_length=20, blank=True)
    education = models.CharField(max_length=20, blank=True)
    direction = models.CharField(max_length=30, blank=True)
    past_evaluation = models.CharField(max_length=100, blank=True)
    desc_achive = models.CharField(max_length=100, blank=True)
    desc_teach_type = models.CharField(max_length=100, blank=True)
    desc_publish = models.CharField(max_length=100, blank=True)
    desc_honor = models.CharField(max_length=100, blank=True)
    desc_more = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.teacher.username

class Student(models.Model):
    student = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=Gender_Choice)
    college = models.CharField(max_length=30)
    major = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.student.username
