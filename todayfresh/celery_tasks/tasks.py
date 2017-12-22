from celery import Celery
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as itdanger
from django.core.mail import send_mail

# 初始化，django的环境
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todayfresh.settings")

# 创建类对象
app = Celery('celery',broker='redis://172.16.183.1:6379/4')

# 定义任务函数
@app.task
def send_register_active_task(mail,token):

    subject = "天天生鲜激活"
    receiver = [mail]
    message = ''
    html_message = '<a href="http://172.16.183.131:8000/user/active/%s" target="_blank">点击激活</a>' % token
    sender = settings.EMAIL_FROM
    send_mail(subject, message, sender, receiver, html_message=html_message)
