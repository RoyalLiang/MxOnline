from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM
from MxOnline.celery import app


@app.task
def send_email(data):
    if data['send_type'] == 'register':
        email_title = '慕学在线网账号激活'
        email_body = '请点击下方链接进行账号激活:http://www.pidouzhu.com/active/{0}'.format(data['code'])
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [data['email']])
        if send_status:
            pass
    elif data['send_type'] == 'forget':
        email_title = '慕学在线网找回密码'
        email_body = '请点击下方链接找回密码:http://www.pidouzhu.com/users/reset/{0}'.format(data['code'])
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [data['email']])
        if send_status:
            pass
    elif data['send_type'] == 'update':
        email_title = '慕学在线网邮箱修改验证码'
        email_body = '您的邮箱验证码为{0}'.format(data['code'])
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [data['email']])
        if send_status:
            pass
