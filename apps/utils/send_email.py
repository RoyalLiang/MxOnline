from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == 'update':
        random_str = generate_random_str(6)
    # elif send_type == 'register':
    #     random_str = generate_random_str(16)
    else:
        random_str = generate_random_str(16)
    email_record.code = random_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    return random_str


def generate_random_str(random_length):
    s = ''
    if random_length == 6:
        chars = '0123456789'
    else:
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789%@&#^*+'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        s += chars[random.randint(0, length)]
    return s


def send_share_email(name, years, email):
    email_title = '慕学在线-用户分享'
    email_body = '我在http://127.0.0.1:8000/org/teacher/list，发现了教师-{0}，对学习中的小伙伴很有帮助，一起来看看吧。金牌讲师，从业年限：{1}年'.format(
        name, years)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass
