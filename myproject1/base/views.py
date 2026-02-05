from xmlrpc.client import FastMarshaller
from django.shortcuts import render,redirect
from .models import CartModel, Products
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):

    if request.user.is_authenticated:
        cartproducts_count = CartModel.objects.filter(host=request.user).count()
    else:
        cartproducts_count = False
    #search operation if there are no records present
    nomatch = False
    trend = False
    offer = False

    #search bar
    if 'q' in request.GET:
        q = request.GET['q']
        all_products = Products.objects.filter(Q(pname__icontains = q) | Q(pdesc__icontains = q))
        # print(len(all_products))
        if len(all_products) == 0:
            nomatch = True
    #category
    elif 'cat' in request.GET:
        cat=request.GET['cat']
        all_products = Products.objects.filter(pcategory=cat)
    #trending product
    elif 'trending' in request.GET:
        all_products = Products.objects.filter(trending=True)
        trend = True
    #offer products
    elif 'offer' in request.GET:
        all_products = Products.objects.filter(offer=True)
        offer = True
    else:
        #to display all products
        all_products = Products.objects.all()

    category = [] #empty
    # a = Products.objects.all()
    for i in Products.objects.all():
        if i.pcategory not in category: #mobile,sports,
            category+=[i.pcategory] 
        


    return render(request,'home.html',{'all_products':all_products,'nomatch':nomatch,'category':category,'cartproducts_count':cartproducts_count,'trend':trend,'offer':offer})

@login_required(login_url='login_')
def addtocart(request,pk):
    product = Products.objects.get(id=pk)
    try:
        cp = CartModel.objects.get(pname=product.pname,host=request.user)
        cp.quantity+=1
        cp.totalprice+=product.price
        cp.save()
        return redirect('home')
    except:    
        CartModel.objects.create(
            pname = product.pname,
            price = product.price,
            pcategory = product.pcategory,
            quantity = 1,
            totalprice = product.price,
            host = request.user
        )
        return redirect('home')

@login_required(login_url='login_')
def cart(request):
    cartproducts_count = CartModel.objects.filter(host=request.user).count()
    print(cartproducts_count)#1
    cartproducts = CartModel.objects.filter(host=request.user)
    TA = 0
    for i in cartproducts:
        # print(i.totalprice)
        TA+=i.totalprice
    # print(TA)#3004500
    return render(request,'cart.html',{'cartproducts':cartproducts,'TA':TA,'profile_nav':True,'cartproducts_count':cartproducts_count})

def remove(request,pk):
    cartproduct = CartModel.objects.get(id=pk)
    cartproduct.delete()
    return redirect('cart')


# def csub(request,pk):
#     cproduct = CartModel.objects.get(id=pk)
#     print(cproduct.pname)
#     if cproduct.quantity > 1:
#         cproduct.quantity-=1
#         cproduct.totalprice-=cproduct.price
#         cproduct.save()
#         return redirect('cart')
#     else:
#         cproduct.delete()
#         return redirect('cart')

def csub(request,pk):
    cproduct = CartModel.objects.get(id=pk)
    print(cproduct.pname)
    
    cproduct.quantity-=1
    cproduct.totalprice-=cproduct.price
    cproduct.save()
    return redirect('cart')



def cadd(request,pk):
    cproduct = CartModel.objects.get(id=pk)
    print(cproduct.pname)
    cproduct.quantity+=1
    cproduct.totalprice+=cproduct.price
    cproduct.save()
    return redirect('cart')