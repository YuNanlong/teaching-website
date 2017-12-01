from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^homepage=(\d+)/$',views.homepage),
    url(r'^add-section=(\d+)/$', views.add_section),
    url(r'^delete-section=(\d+)/$', views.delete_section),
    url(r'^set-top=(\d+)/$', views.set_top),
    url(r'^set-best=(\d+)/$', views.set_best),
    url(r'^delete-post=(\d+)/$', views.delete_post),
    url(r'^delete-reply=(\d+)/$', views.delete_reply),
    url(r'^release-reply=(\(d+))/$', views.release_reply),
    url(r'^release-post=(\d+)/$', views.release_post),
    url(r'^watch_post=(\d+)/$', views.watch_post),
    #url(r'^search-post/$', views.search_post),
    url(r'^download=(\d+)/$', views.download),
]