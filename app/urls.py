# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from views import HomeView, ProfileView, MyProfileView, EditMyProfileView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^profile/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile'),
    url(r'^my-profile/', MyProfileView.as_view(), name='my-profile'),
    url(r'^edit-my-profile/', EditMyProfileView.as_view(), name='edit-my-profile'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}),
    url(r'^admin/import-random-user/$', 'app.admin.import_random_user', name='import-random-user'),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

