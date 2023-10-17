from django.http import HttpResponse
from django.shortcuts import render
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_django
from django.shortcuts import redirect


def index(request):
    return render(request, "index.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("plataforma")
    else:
        if request.method == "GET":
            return render(request, "auth/login.html")
        else:
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = authenticate(email=email, password=password)

            if user:
                login_django(request, user)

                return redirect("org_panel_index")
            else:
                return HttpResponse("Email ou senha invalidos")


# @login_required(login_url="/login/")
# def plataforma(request):
#     if request.user.is_authenticated:
#         return HttpResponse("Plataforma")

@login_required(login_url="/login/")
def org_panel_index(request):
    if request.user.is_authenticated:
        org_name = request.user.org_name
        return render(request, "org_panel/index.html", {"org_name": org_name })
    else:
        return redirect("login")
    
@login_required(login_url="/login/")
def org_panel_contact(request):
    if request.user.is_authenticated:
        org_name = request.user.org_name
        return render(request, "org_panel/contact.html", {"org_name": org_name })
    else:
        return redirect("login")


def register(request):
    if request.user.is_authenticated:
        return redirect("plataforma")
    else:
      if request.method == "GET":
          return render(request, "auth/register.html")
      else:
          username = request.POST.get("username")
          org_name = request.POST.get("org_name")
          email = request.POST.get("email")
          password = request.POST.get("password")

          user = User.objects.filter(email=email).first()

          if user:
              return HttpResponse("Já existe um usuário cadastrado")
          user = User.objects.create_user(username=username, 
              org_name=org_name, email=email, password=password)
          user.save()

          login_django(request, user)

          return redirect("org_panel_index")


def logout(request):
    logout_django(request)
    return redirect("index")
