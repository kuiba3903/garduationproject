from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from User.forms.Userform import UserForm
from User.forms.EmailForm import SendEmailForm
from utils.sendEmail import sendemail
# Create your views here.


def register(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, 'register.html', context={'forms': form})
    print(request.POST)
    form = UserForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True, 'data': '/login/'})
    else:
        print(form.errors)
        return JsonResponse({"status": False, 'error': form.errors})


def send_email(request: HttpRequest):
    form = SendEmailForm(request, data=request.GET)
    email = request.GET["email"]
    tpl = request.GET["tpl"]
    if form.is_valid():
        code = sendemail(email, tpl)
        return JsonResponse({"status": True, "code": code})
    return JsonResponse({"status": False, "error": form.errors})