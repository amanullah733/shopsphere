from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators  import login_required
from base.models import CartModel
import re


# Create your views here.

def login_(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pasw = request.POST['pasw']
        a = authenticate(username = uname, password = pasw)
        if a:
            login(request,a)
            return redirect('home')
        else:
            return render(request,'login_.html',{'error':'Ther usename and password is worng...../'})
    return render(request,'login_.html',{'login_nav':True})

def valid_pasw(pasw):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
    return  re.match(pattern,pasw)

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        uname = request.POST['uname']
        pasw = request.POST['pasw'] #here im fletching that password
        try:
            a = User.objects.get(username = uname)
            return render(request,'register.html',{'error':True})
        except:
            pass

        if not valid_pasw(pasw):
            return render(request,'register.html',{'pasw':'password should be combination...!'})


        a = User.objects.create(
            first_name = fname,
            last_name = lname,
            email = email,
            username = uname,
                
        )
        a.set_password(pasw)
        a.save()
        return redirect(login_)
    return render(request,'register.html',{'login_nav':True})

@login_required(login_url='login_')
def logout_(request):
    logout(request)
    return redirect(login_)

@login_required(login_url='login_')
def profile(request):
    if request.user.is_authenticated:
        cartproductscount = CartModel.objects.filter(host=request.user).count()
    else:
        cartproductscount = False
    return render(request,'profile.html',{'cartproductscount':cartproductscount,'profile_nav':True})


@login_required(login_url='login_')
def reset(request):
    user = request.user
    print(user)

    if request.method == 'POST':

        if 'old_pasw' in request.POST:
            old_pass = request.POST['old_pasw']
            auth_user = authenticate(username = user.username,password = old_pass)
            print(auth_user)

            if auth_user:
                return render(request,'reset.html',{'new_pass':True})
            else:
                return render(request,'reset.html',{'error':True})
            
        if 'new_pasw' in request.POST:   
            new_pasw = request.POST['new_pasw']
            pasw = new_pasw
            if not valid_pasw(pasw):
                return render(request,'reset.html',{'error_pasw':'not a combi'})
            user.set_password(pasw)
            user.save()
            return redirect('login_')
    
    return render(request,'reset.html',{'profile_nav':True})

def new_pasw(request):
    uname = request.session.get('fp_user')

    if uname is None:
        return redirect('forget_pasw')
    
    user = User.objects.get(username = uname)

    if request.method == 'POST':
        new_pasw = request.POST['new_pass']

        user.set_password(new_pasw)
        user.save()

        del request.session['fp_user']
        return redirect('login_')

    return render(request,'new_pasw.html',{'login_nav':True})

def forget_pasw(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        try:
            u = User.objects.get(username = uname)
            request.session['fp_user'] = u.username
            return redirect('new_pasw')
            print(u)
        except User.DoesNotExist:
            return render(request,'forget_pasw.html',{'error':True})

    return render(request,'forget_pasw.html',{'login_nav':True})


@login_required(login_url='login_')
def update(request):
    user = request.user  

    if request.method == 'POST':
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']
        user.username = request.POST['uname']

        user.save()

        return redirect('profile')

    return render(request, 'update.html', {'user': user,'profile_nav':True})
