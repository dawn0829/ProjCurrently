from django.urls import path
from . import views
 
urlpatterns = [
    path('callback', views.callback, name='callback'),
    path('comfirmlogin/<str:lineid>/<str:token>',views.comfirm_login,name='comfirmlogin')
]