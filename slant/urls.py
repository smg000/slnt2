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
from django.views.generic import TemplateView
from slantapp.views import index
from slantapp.views import issue
from slantapp.views import index_test
from slantapp.views import rate
from slantapp.views import why
from slantapp.views import daily_email
from slantapp.views import contact_form
from slantapp.views import thankyou
from slantapp.views import privacy_policy
from slantapp.views import terms_of_service
from slantapp.views import about


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^issue/$', issue),
    url(r'^about/$', about),
    url(r'^rate/$', rate),
    url(r'^why/$', why),
    url(r'^the-daily-skeww/$', daily_email),
    url(r'^contact/$', contact_form),
    url(r'^thank-you/$', thankyou),
    url(r'^index_test/$', index_test),
    url(r'^privacy-policy/$', privacy_policy),
    url(r'^terms-of-service/$', terms_of_service),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]
