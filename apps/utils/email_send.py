# Author Caozy
from users.models import EmailVerifyRecord
import random
from django.core.mail import send_mail
from mxonline.settings import EMAIL_FROM


def random_str(random_length=8):
    str = ''
    str_random = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    for i in range(random_length):
        str += str_random[random.randint(0, len(str_random) - 1)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type=='update':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    email_title = ''
    email_title = ''

    if send_type == 'register':
        email_title = 'NOC在线注册激活链接'
        email_body = '请点击下面链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


    elif send_type == 'forget':
        email_title = 'NOC在线注册密码重置链接'
        email_body = '请点击下面链接重置密码：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'update':
        email_title = 'NOC在线修改邮箱验证码链接'
        email_body = '邮箱验证码为：%s' % code
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
