from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5, max_length=16)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=16)
    # 图片验证码
    captcha = CaptchaField(error_messages={"invalid": '验证码错误'}, required=True)


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    # 图片验证码
    captcha = CaptchaField(error_messages={"invalid": '验证码错误'}, required=True)


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, max_length=16)
    password2 = forms.CharField(required=True, min_length=6, max_length=16)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'phone']
