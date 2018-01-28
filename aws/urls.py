
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from .views import (signin, register,logout_view, aws_submit)


urlpatterns = [
url(r'awssetup/$', aws_submit, name="aws_submit"),
        url(r'^login/', signin, name="login"),
        url(r'^register/' ,register, name="register"),
        url(r'^logout/$',logout_view, name="logout"),

         url(r"^$", TemplateView.as_view(template_name='home.html')),

]