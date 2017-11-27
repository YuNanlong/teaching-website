from django.conf.urls import include, url
from django.contrib import admin
from account import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('account.urls')),
    url(r'^teach/', include('teach.urls')),
    url(r'^home/$', views.home, name="home") # Set main page : /account/base.html
]
