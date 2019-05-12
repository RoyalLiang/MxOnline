from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MxOnline.settings')

# 注册Celery的APP
app = Celery('MxOnline')
# 绑定配置文件
app.config_from_object('django.conf:settings', namespace='CELERY')
app = Celery('MxOnline', backend='redis', broker='redis://127.0.0.1:6379/1')
# 自动发现各个app下的tasks.py文件
app.autodiscover_tasks()
# import djcelery
# from datetime import timedelta
# from celery.schedules import crontab

# djcelery.setup_loader()


# CELERY_TIMEZONE = 'Asia/Shanghai'

# 导入指定的任务模块
# CELERY_IMPORTS = (
#     'users.tasks',
#
# )

# 防止某些情况发生死锁
CELERYD_FORCE_EXECV = True

# 设置worker并发数量
CELERYD_CONCURRENCY = 4

# 允许重试
CELERY_ACKS_LATE = True

# 每个worker最多执行10次任务后销毁
CELERYD_MAX_TASKS_PER_CHILD = 50

# 单个任务最大运行时间
CELERYD_TASK_TIME_LIMIT = 12 * 30
# 定时任务
# CELERYBEAT_SCHEDULE = {
#     'tasks': {
#         'task': 'celery_app.task1.add',
#         'schedule': timedelta(seconds=10),
#         'args': (2, 8),
#     },
#     'tasks1': {
#         'task': 'celery_app.task1.add',
#         'schedule': crontab(hour=19, minute=10),
#         'args': (2, 8),
#     },
#
# }

# 设置celery队列
# CELERY_QUEUES = {
#     'beat_tasks': {
#         'exchange': 'beat_tasks',
#         'exchange_type': 'direct',
#         'binding_key': 'beat_tasks',
#     },
#     'work_queue': {
#         'exchange': 'work_queue',
#         'exchange_type': 'direct',
#         'binding_key': 'work_queue',
#     },
#
# }
#
# CELERY_DEFAULT_QUEUE = 'work_queue'
