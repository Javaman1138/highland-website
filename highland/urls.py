from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = patterns('',
    # use specific views
    url(r'^$', views.HomeView.as_view()),
    url(r'^calendar/$', views.CalendarView.as_view()),
    url(r'^contact$', views.ContactView.as_view()),
    url(r'^meetings/', views.MeetingView.as_view()),
    url(r'^volunteer$', views.VolunteerView.as_view()),
    url(r'^signup-landing/', views.SignUpLandingView.as_view(template_name="landing-signup.html")),
    url(r'^fundraising/', views.GenericView.as_view(template_name="fundraising.html")),
    
    # use alternate urls 
    url(r'^people/', include('people.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^signup/', include('signup.urls')),
    url(r'^remove/', include('signup.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # documents and file uploading
    url(r'^documents/', include('sitedocuments.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
        }),
)
