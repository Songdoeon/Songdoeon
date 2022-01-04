from django.urls import path

from . import views

urlpatterns = [
    path('home/',views.index, name='index'),
    path('select/',views.select, name='select'),
    path('result/',views.result, name='result'),
    path('home/',views.home,name='home'),
    path('detectme/',views.detectme,name='detectme'),


]
