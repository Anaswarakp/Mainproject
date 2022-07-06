"""HR_Managements URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from Crime import admin_urls, user_urls, police_urls, officer_urls
from Crime.views import IndexView, UserRegister, PoliceRegs, Police_officer_reg
from Crime_Report import settings

urlpatterns = [
    path('', IndexView.as_view()),
    path('usereg', UserRegister.as_view()),
    path('policereg', PoliceRegs.as_view()),
    path('officer_reg',Police_officer_reg.as_view()),
    path('admin/',admin_urls.urls()),
    path('police/',police_urls.urls()),
    path('officer/', officer_urls.urls()),

    path('user/',user_urls.urls()),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)