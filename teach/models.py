from django.db import models
from account.models import Teacher, Student
from time import gmtime, strftime
from .storage import FileStorage

def classware_upload_path(instance, filename):
    return '/'.join(['classware', filename])

class Course(models.Model):
    name = models.CharField(max_length=20, unique=True, db_index=True) # 课程名
    textbook = models.CharField(max_length=40, blank=True) # 教材
    week = models.IntegerField() # 周数
    class_time = models.CharField(max_length=30) # 每周的上课时间，例如：周一89节
    abstract = models.CharField(max_length=800, blank=True) # 课程简介，非必需
    credit = models.DecimalField(max_digits=2, decimal_places=1) # 学分，最多两位有效数字和一位小数
    college = models.CharField(max_length=20, blank=True) # 开课学院，非必需
    student = models.ManyToManyField(Student, db_table="take_course") # 上这门课的学生
    teacher = models.ManyToManyField(Teacher, db_table="give_course") # 上这门课的老师

    def __str__(self):
        return self.name

class Plan(models.Model):
    course = models.ForeignKey(Course)
    week_num = models.IntegerField() # 第几周
    topic = models.CharField(max_length=200, blank=True) # 计划内容，非必需
    date = models.DateField() # 上课具体日期

    def __str__(self):
        return self.course.name + str(self.week_num)

class Video(models.Model):
    plan = models.ForeignKey(Plan)
    url = models.URLField() # 视频链接

    def __str__(self):
        return str(self.plan.course.name) + str(self.plan.week_num) + ':' + self.url

class Homework(models.Model):
    plan = models.OneToOneField(Plan)
    deadline = models.DateField() # 截止日期
    mark = models.IntegerField() # 总分
    enclosure = models.FileField(upload_to='homeworks', storage=FileStorage()) # 作业附件
    statement = models.CharField(max_length=800, blank=True) # 作业说明，非必需

    def __str__(self):
        return str(self.plan.course.name) + str(self.plan.week_num)

class Classware(models.Model):
    plan = models.ForeignKey(Plan)
    filename = models.CharField(max_length=100)
    ppt = models.FileField(upload_to=classware_upload_path, storage=FileStorage()) # 课件文件

class Submit(models.Model):
    student = models.ForeignKey(Student)
    homework = models.ForeignKey(Homework)
    comment = models.CharField(max_length=800, blank=True) # 作业备注，非必需
    submit_time = models.DateField(auto_now=True) # 上传时间
    score = models.IntegerField(default=0) # 得分
    solution = models.FileField(upload_to='submits/', storage=FileStorage()) # 作业文件
    remark = models.CharField(max_length=800, blank=True) # 教师评语

class Notice(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=60) # 标题
    content = models.CharField(max_length=800, blank=True) # 内容
    student = models.ManyToManyField(Student, db_table="need_notify") # 尚未被通知的学生
    post_time = models.DateTimeField(auto_now_add=True) # 发布时间

class Comment(models.Model):
    mobile=models.CharField(max_length=20)
    content=models.TextField()

    def __str__(self):
        return self.mobile
