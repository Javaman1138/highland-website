from django.conf.urls.defaults import url

from . import views

urlpatterns = [
    url(r'^$', views.SignUpView.as_view()),
    url(r'^remove/', views.SignUpRemove.as_view()),
    url(r'^landing/', views.SignUpView.as_view(template_name="signup-landing.html")),
]
