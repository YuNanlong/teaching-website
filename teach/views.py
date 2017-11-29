from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *
from account.models import *

@login_required
def teach_detail(request):
    course_name = request.GET['course'] # 获取url中的课程名
    user = request.user
    course = get_object_or_404(Course, name=course_name)
    plan_list = course.plan_set.order_by('week_num')
    # video_list和classware_list都是嵌套的list
    # list中每个元素是一个子list，子list中包含一个week的所有视频和课件资料
    video_list = []
    classware_list = []
    homework_list = []
    for plan in plan_list:
        video = plan.video_set.all()
        if video:
            video_list.append(video)
        else:
            video_list.append([])
        classware = plan.classware_set.all()
        if classware:
            classware_list.append(classware)
        else:
            classware_list.append([])
        if hasattr(plan, 'homework'):
            homework_list.append(plan.homework)
        else:
            homework_list.append([])
    if hasattr(user, 'student') == True:
        if user in course.students.all():
            status = 1
        else:
            status = 0
    elif hasattr(user, 'teacher') == True:  
        if user in course.teachers.all():
            status = 1
        else:
            status = 0
    else:
        status = 0
    return render(request, 'teach_detail.html', {'status': status, 'course': course, 'plan_list': plan_list, 'video_list': video_list, 'classware_list': classware_list, 'homework_list': homework_list})
