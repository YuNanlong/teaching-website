# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404,StreamingHttpResponse
from teach.models import Course
from account.views import home
from django import template
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.

default_section_name = "默认版块"

def getUserType(user):
    if hasattr(user, 'teacher'):
        UserType = "teacher"
    elif hasattr(user, 'student'):
        UserType = "student"
    else:
        UserType = "unknown"
    return UserType

@login_required
def homepage(request, id, status = "true"):
    user = request.user
    try:
        course_id = int(id)
    except ValueError:
        raise Http404()
    try:
        course = Course.objects.get(id = course_id)
    except ValueError:
        raise  Http404()
    course_name = course.name
    sections = Section.objects.all().order_by("id")
    section_list = []
    for section in sections:
        tmp_section = {}
        tmp_section['section_id'] = section.id
        tmp_section['section_name'] = section.name
        tmp_post_list = []
        course_section_posts = Post.objects.filter(course=course,section = section).order_by("-is_top","-time")
        for post in course_section_posts:
            if post.is_best == 0:
                is_best = '普通帖'
            else:
                is_best = '精华帖';
            tmp_post_list.append({'id':post.id,'title':post.title,'poster':post.poster.username,'is_best':is_best,'time':post.time})
        tmp_section['post_list'] = tmp_post_list
        section_list.append(tmp_section)
    #默认板块帖子
    default_section = {}
    default_section['section_id'] = "null"
    default_section['section_name'] = default_section_name
    default_post_list = []
    default_section_posts = Post.objects.filter(course=course,section = models.SET_NULL).order_by("-is_top","-time")
    for post in default_section_posts:
        if post.is_best == 0:
            is_best = '普通帖'
        else:
            is_best = '精华帖';
        default_post_list.append(
            {'id': post.id, 'title': post.title, 'poster': post.poster.username, 'is_best': is_best, 'time': post.time})
    default_section['post_list'] = default_post_list
    section_list.append(default_section)

    instance = {'user':user,'couse_name':course_name,'course_id':course_id,'section_list':section_list,'status':status}
    if request.method == 'POST':
        return render(request, 'homepage.html',instance)
    else:
        return render(request, 'homepage.html',instance)

@login_required
def release_post(request, id):
    try:
        course_id = int(id)
    except ValueError:
        raise Http404()
    try:
        find_the_course = Course.objects.get(id=course_id)
    except ValueError:
        raise Http404()
    if request.method == 'POST':
        title_length = len(request.POST['post_title'])
        content_length = len(request.POST['post_content'])
        error = False
        if title_length <=0 or title_length > 25:
            error = True
        elif content_length <=0 or content_length > 1000:
            error = True
        if error:
            return
        else:
            ptitle = request.POST.get('post_title')
            pcontent = request.POST.get('post_content')
            psectionid = request.POST.get('post_sectionid')
            flag = 0
            try:
                psectionid = int(psectionid)
            except ValueError:
                flag = 1
                psection = models.SET_NULL()
            if flag == 0:
                psection = Section.object.get(id=psectionid)
            pcourse = Course.objects.get(id = id)
            post = Post.objects.create(
                poster=request.user,
                title=ptitle,
                content=pcontent,
                section = psection,
                course = pcourse
            )
            if 'post_file' in request.FILES:
                pfile = request.FILES.get('post_file')
                post.files = pfile
                post.files.name = str(post.id) + '__' + str(pfile.name)
            post.save()
            return homepage(request, course_id, "发帖成功")
    else:
        return homepage(request, course_id, "发帖失败")

@login_required
def watch_post(request,id, status = "true"):
    try:
        post_id = int(id)
    except ValueError:
        raise Http404()
    try:
        the_post = Post.objects.get(id = post_id)
    except ValueError:
        raise Http404()
    post = {'id':the_post.id,'title':the_post.title,'content':the_post.content}
    the_replies = Reply.objects.filter(post = the_post).order_by("time")
    course_id = the_post.course.id
    course_name = the_post.course.name
    no_top = ""
    no_best = ""
    if the_post.is_best > 0:
        no_best = "取消"
    if the_post.is_top > 0:
        no_top = "取消"
    replies = []
    for r in the_replies:
        replies.append({'id': r.id, 'replier': r.replier.username, 'replier_id': r.replier.id, 'content': r.content,'time': r.time})
    instance = {'user':request.user,'course_id':course_id,'course_name':course_name,'post':post,'replies':replies,'no_best':no_best,'no_top':no_top,'status':status}
    if request.method == 'POST':
        return render(request, 'watch_post.html',instance)
    else:
        return render(request, 'watch_post.html',instance)

@login_required
def release_reply(request, id):
    try:
        post_id = int(id)
    except ValueError:
        raise Http404()
    try:
        find_the_post = Post.objects.get(id=post_id)
    except ValueError:
        raise Http404()
    if request.method == 'POST':
        content_length = len(request.POST.get('reply_content'))
        error = False
        if content_length <=0 or content_length > 256:
            error = True
        if error:
            return
        else:
            rcontent = request.POST.get('reply_content')
            reply = Reply.objects.create(
                post=find_the_post,
                replier=request.user,
                content=rcontent,
            )
            reply.save()
            return watch_post(request, post_id, "回帖成功")
    else:
        return watch_post(request, post_id, "回帖失败")

@login_required
def set_top(request,id):
    try:
        post_id = int(id)
    except ValueError:
        raise Http404()
    if request.method == 'GET':
        if getUserType(request.user) != 'teacher':
            return redirect("home")
        try:
            post = Post.objects.get(id=post_id)
        except ValueError:
            raise Http404()
        if post.is_top == 0:
            post.is_top = 1
            prefix = ""
        else:
            post.is_top = 0
            prefix = "取消"
        post.save()
        return watch_post(request,post_id,prefix+"置顶成功")
    else:
        return watch_post(request,post_id,"置顶或取消置顶失败")

@login_required
def set_best(request,id):
    try:
        post_id = int(id)
    except ValueError:
        raise Http404()
    if request.method == 'GET':
        if getUserType(request.user) != 'teacher':
            return redirect("home")
        try:
            post = Post.objects.get(id=post_id)
        except ValueError:
            raise Http404()
        if post.is_best == 0:
            post.is_best = 1
            prefix = ""
        else:
            post.is_best = 0
            prefix = "取消"
        post.save()
        return watch_post(request,post_id,prefix+"加精成功")
    else:
        return watch_post(request,post_id,"加精或取消加精失败")

@login_required
def delete_reply(request,id):
    try:
        post_id = int(id)
    except ValueError:
        raise Http404()
    if request.method == 'POST':
        if getUserType(request.user) != 'teacher':
            return redirect("home")
        reply_id = request.POST.get('reply_id')
        try:
            delreply = Reply.objects.get(id=reply_id)
        except ValueError:
            raise Http404()
        delreply.delete()
        return watch_post(request,post_id,"成功删除回复")
    else:
        return watch_post(request,post_id,"未能删除回复")

@login_required
def delete_post(request,id):
    try:
        post_id = int(id)
    except ValueError:
        raise Http404()
    try:
        delpost = Post.objects.get(id=post_id)
    except ValueError:
        raise Http404()
    course_id = delpost.course.id
    if request.method == 'GET':
        if getUserType(request.user) != 'teacher':
            return redirect("home")
        delpost.delete()
        return homepage(request,course_id,"成功删除帖子")
    else:
        return homepage(request,course_id,"未能删除帖子")

@login_required
def add_section(request):
    try:
        course_id = int(id)
    except ValueError:
        raise Http404()
    try:
        find_the_course = Course.objects.get(id=course_id)
    except ValueError:
        raise Http404()
    if request.method == 'POST':
        if getUserType(request.user) != 'teacher':
            return redirect("home")
        addsection_name = request.POST.get('add_section_name')
        if addsection_name == default_section_name:
            return
        if Section.objects.filter(course = find_the_course, name = addsection_name):
            return
        addtosection = Section.objects.create(
            name = addsection_name,
            course = find_the_course,
        )
        addtosection.save()
        return homepage(request,course_id,"成功添加板块")
    else:
        return homepage(request,course_id,"未能添加板块")

@login_required
def delete_section(request, id):
    try:
        course_id = int(id)
    except ValueError:
        raise Http404()
    try:
        find_the_course = Course.objects.get(id=course_id)
    except ValueError:
        raise Http404()
    if request.method == 'POST':
        if getUserType(request.user) != 'teacher':
            return redirect("home")
        delsection_id = request.POST.get('delete_section_id')
        try:
            delsection_id = int(delsection_id)
        except:
            return
        delsection = Section.objects.get(id = delsection_id)
        delsection.delete()
        return homepage(request,course_id,"成功删除板块")
    else:
        return homepage(request,course_id,"未能删除板块")


@login_required
def download(request,id):
    try:
        offset = int(id)
    except ValueError:
        raise Http404()
    post = Post.objects.get(id=offset)
    filename = post.files.name

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name = post.files.name
    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response
