from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^home', views.teach_home, name="teach_home") # Better to add teach_ prefix to avoid duplicate names
]