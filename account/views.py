from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from .forms import TeacherEditForm, StudentEditForm

@login_required
def edit(request):
    if hasattr(request.user, 'teacher'):
        teacher = request.user.teacher
        if request.method == 'POST':
            form = TeacherEditForm(request.POST)
            if form.is_valid():
                request.user.username = form.cleaned_data['username']
                request.user.email = form.cleaned_data['email']
                teacher.phone = form.cleaned_data['phone']
                teacher.desc_achive = form.cleaned_data['desc_achive']
                teacher.desc_teach_type = form.cleaned_data['desc_teach_type']
                teacher.desc_publish = form.cleaned_data['desc_publish']
                teacher.desc_honor = form.cleaned_data['desc_honor']
                teacher.desc_more = form.cleaned_data['desc_more']
                teacher.save()
                request.user.save()
                return redirect('home')
        else:
            form = TeacherEditForm(
                initial={
                    'username': request.user.username, 
                    'email': request.user.email,
                    'phone': teacher.phone,
                    'desc_achive': teacher.desc_achive,
                    'desc_teach_type': teacher.desc_teach_type,
                    'desc_publish': teacher.desc_publish,
                    'desc_honor': teacher.desc_honor,
                    'desc_more': teacher.desc_more
                }) #加载原始信息
            return render(request, 'teacher_edit.html', {'form': form})
    elif hasattr(request.user, 'student'):
        student = request.user.student
        if request.method == 'POST':
            form = StudentEditForm(request.POST)
            if form.is_valid():
                request.user.username = form.cleaned_data['username']
                request.user.email = form.cleaned_data['email']
                student.phone = form.cleaned_data['phone']
                student.save()
                request.user.save()
                return redirect('home')
        else:
            form = StudentEditForm(
                initial={
                    'username': request.user.username, 
                    'email': request.user.email,
                    'phone': student.phone,
                    }) #加载原始信息
            return render(request, 'student_edit.html', {'form': form})
    else:
        return redirect('home')

@login_required
def change_pwd(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_pwd.html', {'form': form})

# Set as home page without requiring logged in
def home(request):
    return render(request, 'base.html')

# TODO: 帮助页面
# TODO: 重置密码邮件发送
