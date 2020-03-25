from .views import user_list, UserViewSet
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from rest_framework_jwt.views import ObtainJSONWebToken
from .serializers import CustomJWTSerializer

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('page=<int:page>/', user_list, name='list'),
    path('login', ObtainJSONWebToken.as_view(
        serializer_class=CustomJWTSerializer))
]

urlpatterns += router.urls
