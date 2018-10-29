import logging

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from user.models import User
from user.forms import RegisterForm
from common.http import render_json

inf_log = logging.getLogger('inf')
err_log = logging.getLogger('err')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            return redirect('/user/login/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')

        # 取出用户数据
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist as e:
            err_log.error(e)
            return render(request, 'login.html', {'error': '用户不存在'})

        # 检查用户密码
        if check_password(password, user.password):
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['avatar'] = user.icon.url
            inf_log.info('%s login' % user.nickname)
            return redirect('/user/info/')
        else:
            err_log.error('%s password error' % user.nickname)
            return render(request, 'login.html', {'error': '密码错误'})
    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('/')


def user_info(request):
    uid = request.session['uid']
    user = User.objects.get(pk=uid)

    return render_json(user.to_dict())
