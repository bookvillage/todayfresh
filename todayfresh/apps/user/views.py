from django.shortcuts import render,redirect
import re
from apps.user.models import User
from django.views.generic import View
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as itdanger
from itsdangerous import SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
# Create your views here.

def register(request):
    '''显示注册页面'''
    return render(request, 'register.html')


def register_handle(request):
    '''注册处理'''
    # 接收参数
    username = request.POST.get('user_name')
    pwd = request.POST.get('pwd')
    mail = request.POST.get('email')
    repwd = request.POST.get('cpwd')
    allow = request.POST.get('allow')

    # 参数校验
    if not all([username, pwd, mail,repwd]):
        return render(request,'register.html',{'errmsg':'数据不完整'})
    # 校验邮箱
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',mail):
        return render(request, 'register.html', {'errmsg': '邮箱不合法'})
    # 密码校验
    if not pwd ==repwd:
        return render(request, 'register.html', {'errmsg': '两次密码不一致'})
    # 勾选协议
    if not allow == 'on':
        return render(request, 'register.html', {'errmsg': '请阅读协议'})
    # 校验用户名是否存在
    try:
        use = User.objects.get(username = username)
    except use.DoesNotExist:
        use = None
    if use:
        return render(request, 'register.html', {'errmsg': '用户名已经注册'})

    # 业务处理
    user = User.objects.create_user(username,mail,pwd)
    user.is_active = 0
    user.save()

    # 返回应答
    return redirect(reverse('goods:index'))


class RegisterViews(View):
    '''注册'''
    def get(self,request):
        return render(request, 'register.html')

    def post(self,request):
        '''注册处理'''
        # 接收参数
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        mail = request.POST.get('email')
        repwd = request.POST.get('cpwd')
        allow = request.POST.get('allow')

        # 参数校验
        if not all([username, pwd, mail, repwd]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', mail):
            return render(request, 'register.html', {'errmsg': '邮箱不合法'})
        # 密码校验
        if not pwd == repwd:
            return render(request, 'register.html', {'errmsg': '两次密码不一致'})
        # 勾选协议
        if not allow == 'on':
            return render(request, 'register.html', {'errmsg': '请阅读协议'})
        # 校验用户名是否存在
        try:
            obj = User.objects.get(username = username)
        except User.DoesNotExist:
            obj = None
        if obj:
            return render(request, 'register.html', {'errmsg': '用户名已经注册'})

        # 业务处理
        obj = User.objects.create_user(username, mail, pwd)
        obj.is_active = 0
        obj.save()

        # 用户激活
        danger = itdanger(settings.SECRET_KEY,600)
        info = {'confirm':obj.id}
        token = danger.dumps(info).decode()
        subject = "天天生鲜激活"
        receiver = [mail]
        message = '<a href="http://127.0.0.1:8000/user/active/%s" target="_blank">点击激活</a>'% token
        html_message = '<a href="http://127.0.0.1:8000/user/active/%s" target="_blank">点击激活</a>' % token
        sender = settings.EMAIL_FROM
        send_mail(subject,message,sender,receiver,html_message=html_message)

        # 返回应答
        return redirect(reverse('goods:index'))


class ActiveViews(View):
    '''激活'''
    def get(self,request,token):
        danger = itdanger(settings.SECRET_KEY, 600)
        try:
            info = danger.load(token)
            user_id = info['confirm']
            obj = User.objects.get(id=user_id)
            obj.is_active=1
            obj.save()

            return redirect(reverse('user:login'))
        except SignatureExpired:
            # 出了这个异常 激活链接以及失效
            return HttpResponse('激活码已经失效')


class LoginViews(View):
    def get(self,request):
        return render(request,'index.html')