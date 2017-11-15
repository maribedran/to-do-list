from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    url('^$', TemplateView.as_view(template_name='index.html')),
    url('^api/', include('core.urls', namespace='core')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls', namespace='rest_auth')),
    url(r'^rest-auth/registration/',
        include('rest_auth.registration.urls', namespace='registration')),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
]
