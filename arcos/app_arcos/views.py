from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "index.html")

def login(request):
    if request.method == "GET":
        return render(request, "auth/login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login_django(request, user)

            return HttpResponse("autenticado")
        else:
            return HttpResponse("Email ou senha invalidos")

@login_required(login_url="/login/")
def plataforma(request):
    if request.user.is_authenticated:
        return HttpResponse("Plataforma")
    


def register(request):
    if request.method== "GET":
        return render(request,"auth/register.html")
    else:
        username=request.POST.get("username")
        email =request.POST.get("email")
        password =request.POST.get("password")
        
        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse("Já existe um usuário cadastrado")
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        return HttpResponse("usuário cadastrado com sucesso")
    

        