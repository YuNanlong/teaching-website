from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^home', views.teach_detail, name="teach_detail") # Better to add teach_ prefix to avoid duplicate names
]