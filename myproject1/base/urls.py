from django.urls import  path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('addtocart/<int:pk>',addtocart,name='addtocart'),
    path('cart/',cart,name='cart'),
    path('remove/<int:pk>',remove,name='remove'),
    path('csub/<int:pk>',csub,name='csub'),
    path('cadd/<int:pk>',cadd,name='cadd'),
]