from django.http import HttpResponse
from django.shortcuts import render
from .models import Action, Contact, User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_django
from django.shortcuts import redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage





def index(request):
    return render(request, "index.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("org_panel_index")
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
        return render(request, "org_panel/index.html", {"org_name": org_name, "user": request.user })
    else:
        return redirect("org_panel_index")
    
@login_required(login_url="/login/")
def org_panel_contact(request):
    if request.user.is_authenticated:
       if request.method == 'POST':
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        instagram = request.POST.get('instagram')
        facebook = request.POST.get('facebook')
        user = request.user
        try:
            contact = Contact.objects.get(user=user)
            contact.email = email
            contact.phone = telefone
            contact.instagram = instagram
            contact.facebook = facebook
            contact.save()
            messages.success(request, 'Contato atualizado com sucesso!')
        except Contact.DoesNotExist:
            contact = Contact(user=user, email=email, phone=telefone, instagram=instagram, facebook=facebook)
            contact.save()
            messages.success(request, 'Contato criado com sucesso!')
        return redirect('org_panel_contact')
       else:
         
        initial_data = {}
        try:
          contact = Contact.objects.get(user=request.user)
          initial_data = {
          'email': contact.email,
          'phone': contact.phone,
          'instagram': contact.instagram,
          'facebook': contact.facebook
          }
        except Contact.DoesNotExist:
          initial_data = {
          'email': '',
          'phone': '',
          'instagram': '',
          'facebook': ''
          }
        org_name = request.user.org_name
        return render(request, "org_panel/contact.html", {"org_name": org_name, "email": initial_data['email'], "phone": initial_data['phone'], "instagram": initial_data['instagram'], "facebook": initial_data['facebook']})
    else:
        return redirect("login")

@login_required(login_url="/login/")
def org_panel_actions_index(request):
    if request.user.is_authenticated:
        org_name = request.user.org_name
        actions = Action.objects.filter(user=request.user)
        return render(request, "org_panel/actions/index.html", {"org_name": org_name, "actions": actions})
    else:
        return redirect("org_panel_index")
    
@login_required(login_url="/login/")
def org_panel_actions_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
          title = request.POST.get('title')
          description = request.POST.get('description')
          day = request.POST.get('day')
          month = request.POST.get('month')
          year = request.POST.get('year')
          image = request.FILES.get('image')
          attachments = request.FILES.get('attachments')
          user = request.user
          action = Action(user=user, title=title, description=description, day=day, month=month, year=year, image=image, attachments=attachments)
          action.save()
          messages.success(request, 'Ação criada com sucesso!')
        org_name = request.user.org_name
        return render(request, "org_panel/actions/add.html", {"org_name": org_name })
    else:
        return redirect("org_panel_index")
    
@login_required(login_url="/login/")
def org_settings_panel(request):
   
   if request.user.is_authenticated:
      org_name = request.user.org_name

      return render (request, "org_panel/settings.html", {"org_name" : org_name, "is_public" : request.user.is_public})
   else:
      return(redirect("login"))
   
@login_required(login_url="/login/")
def change_visibility (request):
   if request.method == 'POST':
      visibility = request.POST.get('visibility')

      if visibility == 'public':
         request.user.is_public = True

      elif visibility == 'private':
         request.user.is_public = False

      request.user.save()
      messages.success(request, "Visibilidade alterada com sucesso!")
   return redirect ('org_panel_settings')


    
      

def register(request):
    if request.user.is_authenticated:
        return redirect("org_panel_index")
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

def view_site(request, username):
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("site nao encontrado")
    
    return render(request, "view/index.html", {"user": user})

def view_site_actions(request, username):
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("site nao encontrado")
    try:
      actions = Action.objects.filter(user=user)
    except Action.DoesNotExist:

        actions = []
    return render(request, "view/actions.html", {"user": user, "actions": actions})

def view_site_action(request, username, id):
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("site nao encontrado")
    try:
      action = Action.objects.get(user=user, id=id)
    except Action.DoesNotExist:
        return HttpResponse("acao nao encontrada")
    return render(request, "view/action.html", {"user": user, "action": action})

def view_site_contact(request, username):
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("site nao encontrado")
    try:
      contact = Contact.objects.get(user=user)
    except Contact.DoesNotExist:
        return HttpResponse("Contatos não cadastrados")

    return render(request, "view/contact.html", {"user": user, "contact": contact})