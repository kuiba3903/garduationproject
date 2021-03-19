from User.models import User
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from User import models


class loginform(forms.Form):
    email = forms.EmailField(label="Email")
    code = forms.CharField(label="验证码")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        exists = models.User.objects.filter(email=email).exists()
        if not exists:
            raise ValidationError("邮箱不存在")
        return email


class loginimageform(forms.Form):
    name = forms.CharField(label="用户名")
    password = forms.CharField(label="密码", widget=forms.PasswordInput())
    code = forms.CharField(label="图片验证码")

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)

    def clean_code(self):
        code = self.cleaned_data.get("code")
        session_code = self.request.session.get("imagecode")
        if not session_code:
            raise ValidationError("验证码已过期,请重新获取")
        if code != session_code:
            raise ValidationError("验证码输入错误")
        return code


