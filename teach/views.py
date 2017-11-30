from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.forms.formsets import formset_factory
from .models import *
from account.models import *
from .forms import *
import os, sys
from django.http import StreamingHttpResponse

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
        if user in course.student.all():
            status = 1
        else:
            status = 0
    elif hasattr(user, 'teacher') == True:  
        if user in course.teacher.all():
            status = 1
        else:
            status = 0
    else:
        status = 0
    return render(request, 'teach_detail.html', {'status': status, 'course': course, 'plan_list': plan_list, 'video_list': video_list, 'classware_list': classware_list, 'homework_list': homework_list})

@login_required
def teacher_introduction(request):
    teacher_id = request.GET['id']
    teacher_info = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'teacher_introduction.html', {'teacher_info': teacher_info})

@login_required
def edit_schedule(request):
    course_name = request.GET['course']
    course = get_object_or_404(Course, name=course_name)
    if len(course.plan_set.all()) == 0:
        for i in range(course.week):
            plan = Plan(week_num = i + 1, date='2017-01-01', course=course)
            plan.save()
    plan_list = course.plan_set.all()
    PlanFormSet = formset_factory(PlanForm, extra=0)
    if request.method == 'POST':
        formset = PlanFormSet(request.POST)
        if formset.is_valid() == True:
            for form in formset:
                plan = get_object_or_404(plan_list, week_num=form.cleaned_data['week_num'])
                plan.date = form.cleaned_data['date']
                plan.topic = form.cleaned_data['topic']
                plan.save()
            return redirect('home')
    else:
        formset_init = [{'week_num': plan.week_num, 'date': plan.date, 'topic': plan.topic} for plan in plan_list]
        formset = PlanFormSet(initial=formset_init)
    return render(request, 'teacher_schedule.html', {'formset': formset})

@login_required
def check_notice(request):
    user = request.user
    course_list = user.student.course_set.all()
    notice_list = Notice.objects.order_by('-post_time').all()
    related_notice = []
    for notice in notice_list:
        if notice.course in course_list:
            if user.student in notice.student.all():
                notice.student.remove(user.student)
                notice.save()
                notice.is_read = False
            else:
                notice.is_read = True
            related_notice.append(notice)
    return render(request, 'student_notice.html', {'related_notice': related_notice})

@login_required
def upload_classware(request):
    course_name = request.GET['course']
    course = get_object_or_404(Course, name=course_name)
    if request.method == 'POST':
        form = ClasswareForm(request.POST, request.FILES)
        if form.is_valid():
            plan = course.plan_set.filter(week_num=request.POST['week_num'])
            if len(plan) > 0:
                #request.FILES['classware'].name = 'ss'
                classware = Classware(plan=plan[0], ppt=request.FILES['classware'])
                classware.save()
                return redirect('home')
    else:
        form = ClasswareForm()
    return render(request, 'teacher_courseware.html', {'form': form})

@login_required
def download_classware(request):
    filename = request.GET['classware']
    def read_file(filepath, chunk_size=10000):
        file = open(filepath, 'rb')
        while True:
            chunk = file.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break
    response = StreamingHttpResponse(read_file('media/classware/' + str(filename)))
    response['Content-Disposition'] = 'attachment; filename=' + str(filename)
    response['Content-Type'] = 'application/octet-stream'
    return response

@login_required
def delete_classware(request):
    if request.method == 'POST':
        delete_id_list = list(request.POST.items())
        for delete_id in delete_id_list:
            if delete_id[0] != 'csrfmiddlewaretoken':  
                classware = get_object_or_404(Classware, pk=delete_id[1][0])
                classware.delete()
        return redirect('home') 
    else:
        course_name = request.GET['course']
        course = get_object_or_404(Course, name=course_name)
        plan_list = course.plan_set.all()
        classware_list = []
        for plan in plan_list:
            classware_list.extend(plan.classware_set.all())          
        return render(request, 'teacher_courseware_delete.html', {'classware_list': classware_list})

