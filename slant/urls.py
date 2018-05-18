"""slant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from slantapp.views import index
from slantapp.views import index_test
from slantapp.views import why
from slantapp.views import contact_form
from slantapp.views import thankyou

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^why/$', why),
    url(r'^contact/$', contact_form),
    url(r'^thank-you/$', thankyou),
    url(r'^index_test/$', index_test),
]
