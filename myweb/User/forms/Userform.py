from User.models import User
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from User import models


class UserForm(forms.ModelForm):
    phone = forms.CharField(label="手机号", validators=[
        RegexValidator(
            r'^((13[0-9])|(14[5-9])|(15([0-3]|[5-9]))|(16[6-7])|(17[1-8])|(18[0-9])|(19[1|5])|(19[6|8])|(199))\d{8}$',
            "手机号格式错误"),
    ])
    password = forms.CharField(label="密码",
                               min_length=4, error_messages={'min_length': '密码长度不能小于4个字符'},
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="重复密码",min_length=4,
                                       error_messages={'min_length': '密码长度不能小于4个字符'}, widget=forms.PasswordInput())
    code = forms.CharField(label="验证码")

    class Meta:
        model = User
        fields = ['name', 'phone', 'qq', 'password', 'confirm_password', 'email', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)

    def clean_name(self):
        name = self.cleaned_data["name"]
        exists = models.User.objects.filter(name=name).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        exists = models.User.objects.filter(phone=phone).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return phone

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            raise ValidationError("两次输入的密码不一致")
        return confirm_password



