from operator import truth
from django.shortcuts import render,redirect
from .models import Products,CartModel
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        cartproductscount = CartModel.objects.filter(host=request.user).count()
    else:
        cartproductscount = False

    nomatch = False
    trend = False
    offer = False

    if 'q' in request.GET:
        q = request.GET['q']
        all_products = Products.objects.filter(Q(pname__icontains = q)| Q(pdesc__icontains=q))
        print(len(all_products))#0 #2
        if len(all_products) == 0:
            nomatch=True
    elif 'cat' in request.GET:
        cat = request.GET['cat']
        all_products = Products.objects.filter(pcategory = cat)
    elif 'trending' in request.GET:
        all_products = Products.objects.filter(trending = True)
        trend = True
    elif 'offer' in request.GET:
        all_products = Products.objects.filter(offer = True)
        offer = True
    else:
        all_products = Products.objects.all()
    
    list = [] #empty list
    data = Products.objects.all()
    for i in data:#fletching all records 
        if i.pcategory not in list:
            list+=[i.pcategory]

    return render(request,'home.html',{'all_products':all_products,'cartproductscount':cartproductscount,'nomatch':nomatch,'category':list,'trend':trend,'offer':offer})

@login_required(login_url='login_')
def addtocart(request,pk):
    product = Products.objects.get(id=pk)

    try:
        cp = CartModel.objects.get(pname = product.pname,host = request.user)
        cp.quatity+=1
        cp.totalprice+=product.price
        cp.save()
        return redirect('home')
    except:
        CartModel.objects.create(
            pname = product.pname,
            price = product.price,
            pcategory = product.pcategory,
            quatity  = 1,
            totalprice = product.price,
            host = request.user
        )
        return redirect('home')

def cart(request):
    cartproductscount = CartModel.objects.filter(host=request.user).count()
    cartproducts = CartModel.objects.filter(host=request.user)

    TA = 0
    for i in cartproducts:
        # print(i.totalprice)
        TA+=i.totalprice
    print(TA)
    return render(request,'cart.html',{'cartproducts':cartproducts,'TA':TA,'cartproductscount':cartproductscount,'profile_nav':True})

def remove(request,pk):
    data = CartModel.objects.get(id=pk)
    data.delete()
    return redirect('cart')

def sub(request,pk):
    cproduct = CartModel.objects.get(id=pk)
    if cproduct.quatity >1:
        cproduct.quatity-=1
        cproduct.totalprice-=cproduct.price
        cproduct.save()
    else:
        cproduct.delete()
    return redirect('cart')

def add(request,pk):
    cproduct = CartModel.objects.get(id=pk)
    cproduct.quatity+=1
    cproduct.totalprice+=cproduct.price
    cproduct.save()
    return redirect('cart')
