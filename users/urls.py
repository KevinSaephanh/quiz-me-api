from .views import user_list, UserViewSet
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('page=<int:page>/', user_list, name='list'),
]

urlpatterns += router.urls
