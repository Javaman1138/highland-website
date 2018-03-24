from django.conf.urls.defaults import url

from . import views

urlpatterns = [
    url(r'^$', views.EventView.as_view()),
    url(r'^news/item/$', views.NewsItemView.as_view()),
]
