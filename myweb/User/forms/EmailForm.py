from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from User.models import User


class SendEmailForm(forms.Form):
    email = forms.EmailField(label="Email")

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_email(self):
        # email校验的钩子
        email = self.cleaned_data["email"]
        # 校验email模板
        tpl = self.request.GET.get("tpl")
        if not (tpl == "register" or tpl == "login"):
            raise ValidationError("邮箱模板格式错误")
        # 校验数据库里有没有email
        exists = User.objects.filter(email=email).exists()
        if tpl == "register":
            if exists:
                raise ValidationError("邮箱已存在")
        if tpl == "login":
            if not exists:
                raise ValidationError("邮箱不存在")
        return email


