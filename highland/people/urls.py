from django.conf.urls.defaults import url

from . import views

urlpatterns = [
    url(r'^execs$', views.ExecutiveView.as_view()),
    url(r'^chairs$', views.CommitteeChairView.as_view()),
    url(r'^committee$', views.CommitteeView.as_view()),
    url(r'^committee/signup$', views.CommitteeSignUpView.as_view()),
]
