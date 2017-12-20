from celery import Celery


# 创建类对象
Celery('celery',broker='redis://172.16.183.1:6379/4')

# 定义任务函数