from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=20, verbose_name='用户名')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    qq = models.CharField(max_length=20, verbose_name='QQ')
    email = models.EmailField(max_length=30, verbose_name='Email')
    # code = models.CharField(max_length=20, verbose_name='验证码')
    password = models.CharField(max_length=20, verbose_name='密码')
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='创建时间')

    def __str__(self):
        return '用户: {} '.format(self.name)
    class Meta:
        verbose_name = verbose_name_plural = "用户信息"
        db_table = "users"