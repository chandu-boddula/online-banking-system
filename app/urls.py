from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name= "index"),
    path('1',views.create,name="create"),
    path('2',views.pin_gen,name="pin"),
    path('3',views.valid_otp,name="otp"),
    path('4',views.balance,name='bal'),
    path('5',views.withdrawl,name="take"),
    path('6',views.deposit,name='dep'),
    path('7',views.transfer,name="transfer")

    
]