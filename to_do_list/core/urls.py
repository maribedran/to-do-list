from django.conf.urls import url, include
from rest_framework import routers

from core.views import ToDoListViewSet

router = routers.DefaultRouter()
router.register(r'to_do_list', ToDoListViewSet, base_name='to_do_list')

urlpatterns = [
    url(r'^', include(router.urls)),
]
