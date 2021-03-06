from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import (UserRegisterView, DogRetrieveView,
                            UserDogStatusUpdateView, UserPrefUpdateView,
                            DogListCreateView, DogDeleteView)


urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^api/dog/(?P<pk>-?\d+)/(?P<feeling>(\bliked|\bdisliked|\bundecided))/next/$',
        DogRetrieveView.as_view(),
        name='next-dog'),
    url(r'^api/dog/(?P<pk>\d+)/(?P<feeling>(\bliked|\bdisliked|\bundecided))/$',
        UserDogStatusUpdateView.as_view(),
        name='userdog-update'),
    url(r'^api/dog/$',
        DogListCreateView.as_view(),
        name='list-create-dog'),
    url(r'^api/dog/(?P<pk>\d+)/$',
        DogDeleteView.as_view(),
        name='delete-dog'),
    url(r'^api/user/preferences/$',
        UserPrefUpdateView.as_view(),
        name='userpref-update'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html'))
])
