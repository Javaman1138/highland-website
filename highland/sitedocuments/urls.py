from django.conf.urls.defaults import url

from . import views

urlpatterns = [
    url(r'^newsletter$', views.DocumentView.as_view()),
]
