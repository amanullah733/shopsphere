
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from  base.models import CartModel


# Create your views here.
def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(username,password)
        u = authenticate(username=username,password=password)
        # print(u) #None #admin
        if u:
            login(request,u)
            return redirect('home')
        else:
            return render(request,'login_.html',{'status':'entered username or password is wrong'})
    return render(request,'login_.html',{'login_nav':True})


def register(request):
    if request.method == 'POST':
        a = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        # print(a,last_name,email,username,password)
        try:
            u = User.objects.get(username=username)
            return render(request,'register.html',{'status':'username already exist,create the different username....' })
        except:
            u = User.objects.create(
                first_name  = a,  #name from the database = variable where you have fletched the data
                last_name = last_name,
                email = email,
                username = username,
                # password = password
            )
            u.set_password(password)
            u.save()
            return redirect('login_')
    return render(request,'register.html',{'login_nav':True})

@login_required(login_url='login_')
def profile(request):
    cartproducts_count = CartModel.objects.filter(host=request.user).count()
    return render(request,'profile.html',{'profile_nav':True,'cartproducts_count':cartproducts_count})

@login_required(login_url='login_')
def logout_(request):
    logout(request)
    return redirect('login_')


def rest_pass(request):
    cartproducts_count = CartModel.objects.filter(host=request.user).count()
    user = request.user
    print(user)#admin
    if request.method == 'POST':

        if 'oldpasw' in request.POST:
            old_pass = request.POST['oldpasw']
            auth_user = authenticate(username = user.username,password = old_pass)

            if auth_user:
                return  render(request,'rest_pass.html',{'new_pass':True})
            else:
                return  render(request,'rest_pass.html',{'wrong':True})
            
        if 'newpasw' in request.POST:
            new_pasw = request.POST['newpasw']

            if user.check_password(new_pasw):
                return render(request,'rest_pass.html',{'same':True})

            user.set_password(new_pasw)
            user.save()
            return redirect('login_')
    return render(request, 'rest_pass.html',{'profile_nav':True,'cartproducts_count':cartproducts_count})


def forget_pass(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            u = User.objects.get(username=username)
            print(u)
            request.session['fp_user'] = u.username
            return redirect('new_password')
        except User.DoesNotExist:
            return render(request,'forget_pasw.html',{'error':True})

    return render(request,'forget_pasw.html',{'login_nav':True})

def new_password(request):
    username = request.session.get('fp_user')

    if username is None:
        return redirect('forget_pass')
    
    user = User.objects.get(username = username)

    if request.method == 'POST':
        new_pasw = request.POST.get('password')

        if user.check_password(new_pasw):
            return render(request,'new_passw.html',{'error': 'New Password  should not be simmilar to old password'})
        
        user.set_password(new_pasw)
        user.save()

        del request.session['fp_user']
        return redirect('login_')

    return render(request,'new_passw.html',{'login_nav':True})



def updateprofile(request):
    cartproducts_count = CartModel.objects.filter(host=request.user).count()
    data = request.user
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        data.first_name = first_name
        data.last_name = last_name
        data.email = email
        data.save()
        return redirect('profile')

    return render(request,'updateprofile.html',{'profile_nav':True,'cartproducts_count':cartproducts_count})



'''
===>'login_nav':True
login
register
forget
newpass

===>'profile_nav':True
rest_pass
profile
cart
updateprofile
'''