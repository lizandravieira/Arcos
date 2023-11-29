from django.http import HttpResponse
from django.shortcuts import render
from .models import Action, ActionComment, Contact, Donation, DonationsPage, SiteColor, SiteFont, SiteLogo, User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_django
from django.shortcuts import redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.template.response import TemplateResponse


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
        return render(request, "org_panel/index.html", {"org_name": org_name, "user": request.user})
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
                contact = Contact(
                    user=user, email=email, phone=telefone, instagram=instagram, facebook=facebook)
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
            if (not image or not attachments or not title or not description or not day or not month or not year):
              return HttpResponse("Preencha todos os campos")
            else:
              action = Action(user=user, title=title, description=description, day=day,
                              month=month, year=year, image=image, attachments=attachments)
              action.save()
              messages.success(request, 'Ação criada com sucesso!')
        org_name = request.user.org_name
        return render(request, "org_panel/actions/add.html", {"org_name": org_name})
    else:
        return redirect("org_panel_index")


@login_required(login_url="/login/")
def org_panel_actions_delete(request, id):
    action = Action.objects.get(id=id, user=request.user)
    action.delete()
    messages.success(request, 'Ação deletada com sucesso!')
    return redirect('org_panel_actions_index')




@login_required(login_url="/login/")
def org_panel_update_settings(request):
    if request.method == 'POST':
        visibility = request.POST.get('visibility')
        siteColor = request.POST.get('siteColor')
        siteLogo = request.FILES.get('logo')
        siteFont = request.POST.get('font')

        if (siteLogo):
          existsLogo = SiteLogo.objects.filter(user=request.user).first()

          if existsLogo:
              existsLogo.delete()
              site_logo = SiteLogo(user=request.user, logo=siteLogo)
              site_logo.save()
          else:
              site_logo = SiteLogo(user=request.user, logo=siteLogo)
              site_logo.save()

        if siteFont:
          existsFont = SiteFont.objects.filter(user=request.user).first()

          if existsFont:
              existsFont.font = siteFont
              existsFont.save()
          else:
              site_font = SiteFont(user=request.user, font=siteFont)
              site_font.save()

        site_color, created = SiteColor.objects.get_or_create(user=request.user, defaults={'color': siteColor})

        if not created:
            site_color.color = siteColor
            site_color.save() 

        if visibility == 'public':
            request.user.is_public = True

        elif visibility == 'private':
            request.user.is_public = False

        request.user.save()
        messages.success(request, "Ajustes alterados com sucesso!")
    return redirect('org_panel_settings')


@login_required(login_url="/login/")
def org_panel_settings(request):
    org_name = request.user.org_name
    is_public = request.user.is_public
    siteColor = SiteColor.objects.filter(user=request.user).first()
    siteLogo = SiteLogo.objects.filter(user=request.user).first()
    siteFont = SiteFont.objects.filter(user=request.user).first() 
    return render(request, "org_panel/settings.html", {"org_name": org_name, "is_public": is_public, "site_color": siteColor.color, "site_logo": siteLogo, "site_font": siteFont}) 

@login_required(login_url="/login/")
def org_panel_donations_index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        pix = request.POST.get('pix')
        user = request.user
        try:
            donations_page = DonationsPage.objects.get(user=user)
            donations_page.name = name
            donations_page.description = description
            donations_page.pix = pix
            donations_page.save()
            messages.success(
                request, 'Página de doações atualizada com sucesso!')
        except DonationsPage.DoesNotExist:
            donations_page = DonationsPage(
                user=user, name=name, description=description, pix=pix)
            donations_page.save()
            messages.success(request, 'Página de doações criada com sucesso!')
        return redirect('org_panel_donations_index')
    else:
        try:
            donations_page = DonationsPage.objects.get(user=request.user)
            initial_data = {
                'name': donations_page.name,
                'description': donations_page.description,
                'pix': donations_page.pix
            }
        except DonationsPage.DoesNotExist:
            initial_data = {
                'name': '',
                'description': '',
                'pix': ''
            }
        org_name = request.user.org_name
        return render(request, "org_panel/donations/index.html", {"org_name": org_name, "name": initial_data['name'], "description": initial_data['description'], "pix": initial_data['pix']})


@login_required(login_url="/login/")
def org_panel_donations_list(request):
    org_name = request.user.org_name
    donations = Donation.objects.filter(user=request.user)
    return render(request, "org_panel/donations/list.html", {"org_name": org_name, "donations": donations})


@login_required(login_url="/login/")
def org_panel_donations_confirm(request, id):
    donation = Donation.objects.get(id=id, user=request.user)
    donation.confirmed = True
    donation.save()
    messages.success(request, 'Doação confirmada com sucesso!')
    return redirect('org_panel_donations_list')


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



def is_public(view_func):
    def wrap(request, *args, **kwargs):
        username = kwargs.get('username')
        try:
            user = User.objects.get(username=username)
            site_color = SiteColor.objects.filter(user=user).first()
            site_logo = SiteLogo.objects.filter(user=user).first()
            site_font = SiteFont.objects.filter(user=user).first()  
        except User.DoesNotExist:
            return HttpResponse("site nao encontrado")

        if user.is_public:
            response = view_func(request, *args, **kwargs)
            if isinstance(response, TemplateResponse):
                response.context_data['site_color'] = site_color
                response.context_data['site_logo'] = site_logo
                response.context_data['site_font'] = site_font  
            return response
        else:
            return HttpResponse("O Site não é público.")
    return wrap
@is_public
def view_site(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("site nao encontrado")

    return TemplateResponse(request, "view/index.html", {"user": user})


@is_public
def view_site_actions(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("site nao encontrado")
    try:
        actions = Action.objects.filter(user=user)
    except Action.DoesNotExist:

        actions = []
    return TemplateResponse(request, "view/actions.html", {"user": user, "actions": actions})


@is_public
def view_site_action(request, username, id):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("site nao encontrado")
    try:
        action = Action.objects.get(user=user, id=id)
        comments = ActionComment.objects.filter(action=action)
        
        if request.method == 'POST':
          name = request.POST.get('name')
          comment_text = request.POST.get('comment')
          comment = ActionComment(name=name, text=comment_text, action=action, user=user)
          comment.save()
          messages.success(request, 'Comentário adicionado com sucesso!')
          return redirect('view_site_action', username=username, id=id)
    except Action.DoesNotExist:
        return HttpResponse("acao nao encontrada")
    return TemplateResponse(request, "view/action.html", {"user": user, "action": action, "comments": comments})


@is_public
def view_site_contact(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("site nao encontrado")
    try:
        contact = Contact.objects.get(user=user)
    except Contact.DoesNotExist:
        return HttpResponse("Contatos não cadastrados")

    return TemplateResponse(request, "view/contact.html", {"user": user, "contact": contact})


@is_public
def view_site_donate(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("site nao encontrado")
    try:
        donations_page = DonationsPage.objects.get(user=user)
    except DonationsPage.DoesNotExist:
        return HttpResponse("Página de doações não cadastrada")
    if request.method == 'POST':
        print(request.POST)
        value = request.POST.get('value')
        name = request.POST.get('name')
        cpf = request.POST.get('cpf')
        donation = Donation(user=user, value=value, name=name, cpf=cpf)
        donation.save()
        messages.success(request, 'Doação realizada com sucesso!')
        return redirect('view_site_donate', username=username)
    else:
        return TemplateResponse(request, "view/donate.html", {"user": user, "donations_page": donations_page})


@is_public
def view_site_donations(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("site nao encontrado")
    try:
        cpf = request.GET.get('cpf')
        donations = Donation.objects.filter(user=user, cpf=cpf)
    except Donation.DoesNotExist:
        return HttpResponse("Doações não encontradas")
    return TemplateResponse(request, "view/donations.html", {"user": user, "donations": donations})
