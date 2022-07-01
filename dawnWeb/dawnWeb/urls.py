"""dawnWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from ecgwebsite import views
from register import views as v

urlpatterns = [
    path('', include('pwa.urls')),
    path('admin/', admin.site.urls),
    path('register/',v.register,name="register"),
    path('', include('django.contrib.auth.urls')),
    path('', views.frontend, name="frontend"),
    path('backend/',views.backend, name="backend"),
    path('add/',views.add, name="add"),
    path('analysis/',views.analysispage, name="analysis"),
    path('history/',views.history, name="history"),
    path('quiz/',views.quiz, name="quiz"),
    path('exercise/',views.exercise, name="exercise"),
    path('meditation/',views.meditation, name="meditation"),
    path('guide/',views.guide, name="guide"),path('usetool/',views.usetool, name="usetool"),
    path('detect/',views.detect,name="detect"),
    path('',include('lineNotify.urls')),
    path('delete_rec/', views.delete_rec, name="delete_rec"),
]
