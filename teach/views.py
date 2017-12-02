from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.forms.formsets import formset_factory
from .models import *
from account.models import *
from .forms import *
import os, sys
from django.http import StreamingHttpResponse


def teach_detail(request):
    course_name = request.GET['course']  # 获取url中的课程名
    user = request.user
    course = get_object_or_404(Course, name=course_name)
    plan_list = course.plan_set.order_by('week_num')
    plan_range = len(plan_list)
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
            homework_list.append(None)
    if hasattr(user, 'student') == True:
        if user.student in course.student.all():
            status = 1
        else:
            status = 0
    elif hasattr(user, 'teacher') == True:
        if user.teacher in course.teacher.all():
            status = 1
        else:
            status = 0
    else:
        status = 0
    teach_detail_info = zip(plan_list, classware_list, video_list, homework_list)
    return render(request, 'teach_detail.html',
                  {'status': status, 'course': course, "teach_detail_info": teach_detail_info})


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
            plan = Plan(week_num=i + 1, date='2017-01-01', course=course)
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
            return HttpResponse("<script>alert('提交计划成功!'); window.location.href='/teach/edit_schedule?course=" + course_name + "';</script>")
        return HttpResponse(
            "<script>alert('内部错误!'); window.location.href='/teach/edit_schedule?course=" + course_name + "';</script>")
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
    if request.method == 'POST':
        course_name = request.POST['course']
        course = get_object_or_404(Course, name=course_name)
        form = ClasswareForm(request.POST, request.FILES)
        if form.is_valid():
            plan = course.plan_set.filter(week_num=request.POST['week_num'])
            if len(plan) > 0:
                classware = Classware(plan=plan[0], ppt=request.FILES['classware'])
                classware.save()
        return HttpResponse(
            "<script>window.location.href='/teach/upload_classware?course=" + course_name + "';</script>")
    else:
        course_name = request.GET['course']
        course = get_object_or_404(Course, name=course_name)
        form = ClasswareForm()
        return render(request, 'teacher_courseware.html', {'form': form, 'course': course})


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

    response = StreamingHttpResponse(read_file('media/' + str(filename)))
    response['Content-Disposition'] = 'attachment; filename=' + str(filename)
    response['Content-Type'] = 'application/octet-stream'
    return response


@login_required
def delete_classware(request):
    if request.method == 'POST':
        delete_id_list = request.POST.getlist('deleteList')
        for delete_id in delete_id_list:
            # if delete_id[0] != 'csrfmiddlewaretoken':
            classware = get_object_or_404(Classware, pk=delete_id)
            classware.delete()
        return HttpResponse(True)
    else:
        course_name = request.GET['course']
        course = get_object_or_404(Course, name=course_name)
        plan_list = course.plan_set.all()
        classware_list = []
        for plan in plan_list:
            classware_list.extend(plan.classware_set.all())
        return render(request, 'teacher_courseware_delete.html', {'classware_list': classware_list})


@login_required
def check_homework(request):
    total_point = 0.0
    max_point = 0.0
    min_point = 1000.0
    count = 0
    avg = 0.0
    homework_id = request.GET['id']
    homework = get_object_or_404(Homework, pk=homework_id)
    submit_list = homework.submit_set.all()
    for submit in submit_list:
        if submit.score != 0:
            total_point += submit.score
            count += 1
            if submit.score > max_point:
                max_point = submit.score
            if submit.score < min_point:
                min_point = submit.score
    if count != 0:
        avg = total_point / count
    else:
        min_point = 0.0
    SubmitFormSet = formset_factory(SubmitForm, extra=0)
    if request.method == 'POST':
        formset = SubmitFormSet(request.POST)
        if formset.is_valid() == True:
            for form in formset:
                submit = get_object_or_404(submit_list, pk=form.cleaned_data['submit_id'])
                submit.score = form.cleaned_data['score']
                submit.remark = form.cleaned_data['remark']
                submit.save()
        return HttpResponse(
            "<script>alert('提交成功!');window.location.href='/teach/check_homework?id=" + homework_id + "'</script>")
    else:
        formset_init = [{'submit_id': submit.id, 'score': submit.score, 'remark': submit.remark} for submit in
                        submit_list]
        formset = SubmitFormSet(initial=formset_init)
        # for submit in submit_list:
        #     print(submit.score)
        check_homework_info = zip(formset, submit_list)
        # check_homework_range = range(0, len(submit_list))
        return render(request, 'teacher_homework_correct.html',
                      {'check_homework_info': check_homework_info, 'homework': homework,
                       "count": count, "avg": avg, "max": max_point, "min": min_point, "form_num": len(submit_list)})


def friendly_link(request):
    return render(request, "friendly_link.html")


def help_page(request):
    return render(request, "help.html")


def get_unread_message_number(request):
    if not request.user.is_authenticated() or hasattr(request.user, 'teacher'):
        return HttpResponse(0)
    count = 0
    user = request.user
    course_list = user.student.course_set.all()
    notice_list = Notice.objects.order_by('-post_time').all()
    for notice in notice_list:
        if notice.course in course_list:
            if user.student in notice.student.all():
                count += 1
    return HttpResponse(count)


@login_required
def upload_submit(request):
    student = request.user.student
    if request.method == 'GET':
        course_name = request.GET['course_name']
        week_num = request.GET['week_num']
        course = Course.objects.get(name=course_name)
        plan = course.plan_set.get(week_num=week_num)
        homework = plan.homework
        submit = Submit.objects.filter(student=student, homework=homework)
        dic = {
            'course_name': course_name,
            'week_num': week_num,
            'deadline': homework.deadline,
            'status': True if submit.exists() else False,
            'score': submit.latest('id').score if submit.exists() else 0,
            'comment': submit.latest('id').remark if submit.exists() else '',
            'homework': homework
        }
        return render(request, 'student_homework.html', dic)
    else:
        course_name = request.POST['course_name']
        week_num = request.POST['week_num']
        solution = request.FILES['homework']
        message = request.POST['message']
        course = Course.objects.get(name=course_name)
        plan = course.plan_set.get(week_num=week_num)
        homework = plan.homework
        submit = Submit()
        submit.homework = homework
        submit.solution = solution
        submit.student = student
        submit.comment = message
        submit.save()
        return HttpResponse("<script>alert('作业提交成功!');window.location.href='/teach/upload_submit?course_name="+course_name+"&week_num="+week_num+"';</script>")


@login_required
def download_submit(request):
    id = request.GET['id']
    submit = Submit.objects.get(id=id)
    name = submit.solution.name

    def read_file(filepath, chunk_size=10000):
        file = open(filepath, 'rb')
        while True:
            chunk = file.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break

    response = StreamingHttpResponse(read_file('media/' + str(name)))
    response['Content-Disposition'] = 'attachment; filename=' + str(name)
    response['Content-Type'] = 'application/octet-stream'
    return response


@login_required
def download_homework(request):
    id = request.GET['id']
    homework = Homework.objects.get(id=id)
    name = homework.enclosure.name

    def read_file(filepath, chunk_size=10000):
        file = open(filepath, 'rb')
        while True:
            chunk = file.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break

    response = StreamingHttpResponse(read_file('media/' + str(name)))
    response['Content-Disposition'] = 'attachment; filename=' + str(name)
    response['Content-Type'] = 'application/octet-stream'
    return response


@login_required
def teacher_announce(request):
    if request.method == 'GET':
        course_name = request.GET['course_name']
        dic = {
            'course_name': course_name
        }
        return render(request, 'teacher_announce.html', dic)
    if request.method == 'POST':
        course_name = request.POST['course_name']
        title = request.POST['title']
        content = request.POST['content']
        course = Course.objects.get(name=course_name)
        notice = Notice()
        notice.course = course
        notice.title = title
        notice.content = content
        notice.save()
        students = course.student.all()
        for student in students:
            notice.student.add(student)
        notice.save()
        return HttpResponse(
            "<script>alert('提交成功！'); window.location.href='/teach/teacher_announce?course_name=" + course_name + "';</script>")


@login_required
def upload_homework(request):
    if request.method == 'GET':
        course_name = request.GET['course_name']
        week_num = request.GET['week_num']
        dic = {
            'course_name': course_name,
            'week_num': week_num
        }
        return render(request, 'teacher_homework.html', dic)
    else:
        course_name = request.POST['course_name']
        week_num = request.POST['week_num']
        course = Course.objects.get(name=course_name)
        plan = course.plan_set.get(week_num=week_num)
        try:
            tmp_homework = Homework.objects.get(plan=plan)
            if tmp_homework is not None:
                tmp_homework.delete()
        except:
            print("nothing")
        homework = Homework()
        homework.plan = plan
        homework.enclosure = request.FILES['enclosure']
        homework.statement = request.POST['statement']
        homework.mark = request.POST['mark']
        homework.deadline = request.POST['deadline']
        homework.save()
        return HttpResponse("<script>alert('添加作业成功!');window.location.href='/teach/upload_homework?course_name="+course_name+"&week_num="+week_num+"';</script>")

@login_required
def upload_video(request):
    if request.method == 'GET':
        course_name = request.GET['course_name']
        course = Course.objects.get(name=course_name)
        dic = {
            'course_name': course_name,
            'week': course.week
        }
        return render(request, 'teacher_video.html', dic)
    else:
        course_name = request.POST['course_name']
        week_num = request.POST['week_num']
        course = Course.objects.get(name=course_name)
        plan = Plan.objects.get(course=course, week_num=week_num)
        url = request.POST['url']
        Video.objects.create(plan=plan, url=url)
        return HttpResponse(
            "<script>alert('视频提交成功!');window.location.href='/teach/upload_video?course_name=" + course_name + "';</script>")

def leave_comment(request):
    if request.method == 'POST':
        mobile=request.POST['contract']
        content=request.POST['message']
        Comment.objects.create(mobile=mobile,content=content)
        return HttpResponse("<script>alert('留言成功!我们会尽快给你答复!'); window.location.href='/teach/leave_comment/';</script>")
    else:
        return render(request, 'visitor_message.html')


@login_required
def delete_video(request):
    if request.method == 'GET':
        course_name = request.GET['course_name']
        videoIds = [video for video in Video.objects.all()]
        dic = {
            'course_name': course_name,
            'video': videoIds
        }
        return render(request, 'teacher_video_delete.html', dic)
    else:
        videoIds = request.POST.getlist('deleteList')
        # print(videoIds)
        for videoId in videoIds:
            if Video.objects.filter(id=videoId).exists():
                video = Video.objects.get(id=videoId)
                video.delete()
        return HttpResponse(1)

