from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout 
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . models import *


# Create your views here.
def client_login(request):
    message = request.GET.get('message')
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('clientdashboard')
        else:
            message = "Username or password is incorrect"
            return redirect(reverse('login') + f'?message={message}')
    return render(request, 'login.html', {'message': message})

def admin_login(request):
    message = request.GET.get('message')
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=username, password=pass1)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admindashboard')
        else:
            message = "Username or password is incorrect or user is not admin"
            return redirect(reverse('admin_login') + f'?message={message}')
    return render(request, 'Admin_login.html', {'message' : message})

def signup(request):
    message = request.GET.get('message')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            message = "Your password and comfirm password are not the same"
            return redirect(reverse('signup') + f'?message={message}')
        elif User.objects.filter(username=username).exists():
            message = "Username already taken, Choose another one"
            return redirect(reverse('signup') + f'?message={message}')
        elif User.objects.filter(email=email).exists():
            message = "Email exists already, use another one, or Login"
            return redirect(reverse('signup') + f'?message={message}')
        else:
            my_user = User.objects.create_user(username,email,pass1)  
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html', {'message': message})

def adminlogout(request):
    auth_logout(request)
    return redirect('admin_login')

def clientlogout(request):
    auth_logout(request)
    return redirect('login')

def terms(request):
    return render(request, 't&c.html') 

@login_required
def clientdashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    account = Emmergency_Fund_Account.objects.filter(user=request.user).order_by('-id').first()
    mydict = {
        'account':account,
        'profile':profile
    }
    if request.method == 'POST':
        type = request.POST.get('type')
        balance = request.POST.get('balance')
        EFA = Emmergency_Fund_Account.objects.create(
            user = request.user,
            account_type = type,
            balance = balance
        )
        EFA.save()
        return redirect('clientdashboard')
    return render(request, 'Client_dashboard.html', mydict) 

@login_required
def admindashboard(request):
    query = request.GET.get('q')
    querry = request.GET.get('a')
    if query:
        profiles = Profile.objects.filter(first_name__icontains = query, verified = False).order_by('-id')
    else:
        profiles = Profile.objects.filter(verified = False).order_by('-id')
    if querry:
        actives = Profile.objects.filter(first_name__icontains = querry, verified = True).order_by('-id')
    else:
        actives = Profile.objects.filter(verified = True).order_by('-id')
    my_dict = {
        'profiles':profiles,
        'actives':actives,
        'query':query,
        'querry':querry
    }
    return render(request, 'Admin_dashboard.html', my_dict)  

@login_required
def admintickets(request):
    tickets = Ticket.objects.filter(viewed = False).order_by('-id')
    for ticket in tickets:
        ticket.profile = Profile.objects.get(user = ticket.user)
        ticket.responses = Ticket_Response.objects.filter(ticket=ticket)
    my_dict = {
        'tickets':tickets
    }
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket')
        ticket = Ticket.objects.get(id=ticket_id) 
        respo = request.POST.get('ticket-message')
        response = Ticket_Response.objects.create(
            user = request.user,
            ticket = ticket,
            response = respo
        )
        response.save()
        ticket.viewed = True
        ticket.save()
        return redirect('admintickets')
    return render(request, 'Admin_view_tickets.html',my_dict)

@login_required
def adminviewprofile(request, pk):
    profile = Profile.objects.get(id=pk)
    accounts = Emmergency_Fund_Account.objects.filter(user=profile.user).order_by('-id')
    ticket_no = Ticket.objects.filter(user = profile.user).count()
    my_dict = {
        'profile':profile,
        'accounts':accounts,
        'ticket_no':ticket_no 
    } 
    return render(request, 'Admin_view_profile.html', my_dict)

@login_required
def adminapprovefundaccount(request, pk):
    fund_account = Emmergency_Fund_Account.objects.get(id=pk)
    fund_account.status = True
    fund_account.save()
    profile=Profile.objects.get(user = fund_account.user)
    return redirect('adminviewprofile', pk=profile.id)

@login_required
def adminrejectfundaccount(request, pk):
    fund_account = Emmergency_Fund_Account.objects.get(id=pk)
    fund_account.status = False
    fund_account.save()
    profile=Profile.objects.get(user = fund_account.user)
    return redirect('adminviewprofile', pk=profile.id)

@login_required
def adminverifyprofile(request, pk):
    profile = Profile.objects.get(id=pk)
    profile.verified = True
    profile.save() 
    my_dict = {
        'profile':profile 
    }
    return redirect('admindashboard')

@login_required
def adminapproveprofile(request, pk):
    profile = Profile.objects.get(id=pk)
    profile.verified = True
    profile.save() 
    my_dict = {
        'profile':profile 
    }
    return redirect('adminviewprofile', pk=profile.id)

@login_required
def admindissprofile(request, pk):
    profile = Profile.objects.get(id=pk)
    profile.verified = False
    profile.save() 
    my_dict = {
        'profile':profile 
    }
    return redirect('adminviewprofile', pk=profile.id) 

@login_required
def admindeleteaccount(request, pk):
    profile = Profile.objects.get(id=pk)
    user = profile.user
    user.delete() 
    return redirect('admindashboard')

@login_required
def adminrejectprofile(request, pk):
    profile = Profile.objects.get(id=pk)
    profile.verified = False
    profile.save()
    return redirect('admindashboard')

@login_required
def adminviewprofiletickets(request, pk):
    profile = Profile.objects.get(id=pk)
    tickets = Ticket.objects.filter(user=profile.user).order_by('-id')
    for ticket in tickets:
        ticket.responses = Ticket_Response.objects.filter(ticket=ticket).order_by('-id')
    accounts = Emmergency_Fund_Account.objects.filter(user=profile.user).order_by('-id')
    my_dict = {
        'profile':profile,
        'tickets':tickets,
        'accounts':accounts,
    }
    if request.method == 'POST':
        respo = request.POST.get('response')
        ticket_id = request.POST.get('ticket')
        tick = Ticket.objects.get(id = ticket_id)
        respond = Ticket_Response.objects.create(
            user = request.user,
            ticket = tick,
            response = respo
        )
        respond.save()
        return redirect('adminviewprofiletickets', pk = profile.id)
    return render(request, 'Admin_view_profile_tickets.html', my_dict)

@login_required
def admindissprof(request, pk):
    profile = Profile.objects.get(id=pk)
    profile.verified = False
    profile.save() 
    my_dict = {
        'profile':profile 
    }
    return redirect('adminviewprofiletickets', pk=profile.id) 

@login_required
def adminapproveprof(request, pk):
    profile = Profile.objects.get(id=pk)
    profile.verified = True
    profile.save() 
    my_dict = {
        'profile':profile 
    }
    return redirect('adminviewprofiletickets', pk=profile.id)

@login_required
def adminrejectfund(request, pk):
    fund_account = Emmergency_Fund_Account.objects.get(id=pk)
    fund_account.status = False
    fund_account.save()
    profile=Profile.objects.get(user = fund_account.user)
    return redirect('adminviewprofiletickets', pk=profile.id)

@login_required
def adminapprovefund(request, pk):
    fund_account = Emmergency_Fund_Account.objects.get(id=pk)
    fund_account.status = True
    fund_account.save()
    profile=Profile.objects.get(user = fund_account.user)
    return redirect('adminviewprofiletickets', pk=profile.id)

@login_required
def clientprofile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    mydict = {
        'profile': profile
    }
    if request.method == 'POST':
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.country = request.POST.get('location')
        profile.income_source = request.POST.get('income')
        profile.phone = request.POST.get('phone')
        profile.job_title = request.POST.get('title')
        if request.POST.get('age'):
            profile.dob = request.POST.get('age')
        if request.FILES.get('pp'):
            profile.profile_pic = request.FILES.get('pp')
        if request.FILES.get('Nid'):
            profile.national_id = request.FILES.get('Nid')
        profile.save()
        return redirect('clientprofile')
    return render(request, 'Profile_client.html', mydict)

@login_required
def clienttickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-id')
    response = None
    for ticket in tickets:
        ticket.responses = Ticket_Response.objects.filter(ticket = ticket)

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    mydict = {
        'profile' : profile,
        'tickets' : tickets,
        'response' : response
    }
    if request.method == 'POST':
        reason = request.POST.get('reason')
        statement = request.POST.get('statement')
        ticket = Ticket.objects.create(
            user = request.user,
            type = reason,
            message = statement,
        )
        ticket.save()
        return redirect('clienttickets')
    return render(request, 'Tickets.html', mydict)
