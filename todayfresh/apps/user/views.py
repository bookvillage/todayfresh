from django.shortcuts import render,redirect
import re
from apps.user.models import User, Address
from django.views.generic import View
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as itdanger
from itsdangerous import SignatureExpired
from django.conf import settings
from celery_tasks.tasks import send_register_active_task
from django.contrib.auth import authenticate, login, logout



# Create your views here.



class RegisterViews(View):
    '''注册'''
    def get(self,request):
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
            check = 'checked'
        else:
            username = ''
            check = ''
        return render(request, 'register.html',{'username':username,"checked":check})

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

        danger = itdanger(settings.SECRET_KEY, 300)
        info = {'confirm': obj.id}
        token = danger.dumps(info).decode()

        # 交给celery发送邮件
        send_register_active_task.delay(mail,token)
        # 用户激活
        # danger = itdanger(settings.SECRET_KEY,600)
        # info = {'confirm':obj.id}
        # token = danger.dumps(info).decode()
        # subject = "天天生鲜激活"
        # receiver = [mail]
        # message = '<a href="http://127.0.0.1:8000/user/active/%s" target="_blank">点击激活</a>'% token
        # html_message = '<a href="http://172.16.183.130:8000/user/active/%s" target="_blank">点击激活</a>' % token
        # sender = settings.EMAIL_FROM
        # send_mail(subject,message,sender,receiver,html_message=html_message)


        # 返回应答
        return redirect(reverse('goods:index'))


class ActiveViews(View):
    '''激活'''
    def get(self,request,token):
        danger = itdanger(settings.SECRET_KEY, 300)
        try:
            info = danger.loads(token)
            user_id = info['confirm']
            obj = User.objects.get(id=user_id)
            obj.is_active=1
            obj.save()

            return redirect(reverse('user:login'))
        except SignatureExpired:
            # 出了这个异常 激活链接已经失效
            return render(request, 'register.html', {'errmsg': '激活码过期'})


class LoginViews(View):
    def get(self,request):
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
            checkbox = 'checked'
        else:
            username = ''
            checkbox = ''
        return render(request,'login.html',{'username':username,'checkbox':checkbox})

    def post(self,request):
        # 接收
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        checkbox = request.POST.get('checkbox')
        # 校验
        if not all([username,pwd]):
            return render(request,'login.html',{'errmsg':'数据不全'})
        # 处理
        user = authenticate(username=username, password=pwd)
        if user is None:
            return render(request,'login.html', {'errmsg':'密码或账号不正确'})
        if user.is_active == 0:
            return render(request, 'login.html', {'errmsg':'未激活'})
        # 默认接收到首页，得到next接收next
        next_url = request.GET.get('next',reverse('goods:index'))
        response = redirect(next_url)
        login(request, user)
        if checkbox =='on':
            response.set_cookie('username', username, max_age=3600)
        else:
            response.delete_cookie('username')
        return response

class LogoutViews(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('goods:index'))

from utils.Login_verify import LoginVerify
class UsercenterInfoViews(LoginVerify,View):
    def get(self,request):
        # 获取用户
        user = request.user
        # 获取地址
        address = Address.object.get_default_default(user)
        # 获取用户最近浏览的目录
        return render(request,'user_center_info.html',{'I_active':'active','user':user,'address':address})

class UsercenterOrderViews(LoginVerify,View):
    def get(self,request):
        return render(request,'user_center_order.html',{'O_active':'active'})

class UsercenterSiteViews(LoginVerify,View):
    def get(self,request):
        # 获取用户的默认地址
        user = request.user
        address = Address.object.get_default_default(user)
        # try:
        #     address = Address.objects.get(user=user,is_default=True)
        # except Address.DoesNotExist:
        #     # 用户不存在默认地址
        #     address = None
        request.GET.get('')

        return render(request,'user_center_site.html',{'S_active':'active','address':address})
    def post(self,request):
        # 接收
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        # 校验
        if not all([receiver,addr,phone]):
            return render(request,'user_center_site.html',{'errmsg':'数据不完整'})
        # 处理
        user = request.user
        address = Address.object.get_default_default(user)
        # try:
        #     address = Address.objects.get(user=user,is_default=True)
        # except Address.DoesNotExist:
        #     # 用户不存在默认地址
        #     address = None
        is_default = True
        if address:
            is_default = False

        Address.objects.create(
            user = user,
            receiver = receiver,
            addr = addr,
            zip_code = zip_code,
            phone = phone,
            is_default = is_default
        )
        return redirect(reverse('user:UsercenterSiteViews'))

        # 返回