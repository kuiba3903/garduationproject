from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from User.forms.loginform import loginform, loginimageform
from User.models import User

# Create your views here.


def log_in(request):
    if request.method == "GET":
        form = loginform()
        return render(request, 'login.html', context={'forms': form})
    form = loginform(data=request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"]
        user_object = User.objects.filter(email=email).first()
        request.session["user_id"] = user_object.id
        request.session.set_expiry(60 * 60 * 24)
        return JsonResponse({"status": True, "data": "/index/"})
    print(form.errors)
    return JsonResponse({"status": False, "error": form.errors})


def login_name(request):
    if request.method == "GET":
        form = loginimageform(request)
        return render(request, 'login_name.html', {'forms': form})
    form = loginimageform(request, data=request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        password = form.cleaned_data["password"]
        user_object = User.objects.filter(name=name, password=password).first()
        if user_object:
            request.session["user_id"] = user_object.id
            request.session.set_expiry(60*60*24)
            return redirect('index')
        form.add_error("name", "用户名或者密码输入错误")
    return render(request, 'login_name.html', {'forms': form})



def image_code(request:HttpRequest):
    # 生成图片验证码
    from io import BytesIO
    from utils.imagecode import check_code
    image, code = check_code()
    stream = BytesIO()
    image.save(stream, 'png')
    request.session["imagecode"] = code
    request.session.set_expiry(60)
    return HttpResponse(stream.getvalue())


def logout(requset):
    requset.session.flush()
    return redirect('index')
