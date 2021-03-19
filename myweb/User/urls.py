from django.urls import path
from User.views.login import log_in, login_name, image_code, logout
from User.views.register import register, send_email

urlpatterns = [
    path('login/', log_in, name="login"),
    path('register/', register, name="register"),
    path('send/email', send_email, name="send_email"),
    path('image/code/', image_code, name="image_code"),
    path('login/name/', login_name, name="login_name"),
    path('logout/', logout, name="logout")

]