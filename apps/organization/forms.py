from django import forms
from operation.models import *
import re


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        MOBILE = "^1[358]\d{9}$|^147\d{8}&|^17[67]\d{8}$|^18[6789]\d{8}$|^199\d{8}"
        p = re.compile(MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')


class EmailForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={"invalid": '邮箱输入错误'})
