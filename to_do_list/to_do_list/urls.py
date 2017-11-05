from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url('^', include('core.urls', namespace='core')),
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls', namespace='rest_auth')),
    url(r'^rest-auth/registration/',
        include('rest_auth.registration.urls', namespace='registration')),
]
