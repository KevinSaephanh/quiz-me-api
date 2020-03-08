from .views import create_profile, profile_list, get_profile_by_username, update_delete_profile
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('create/<slug:username>/', create_profile, name='create'),
    path('<int:page>/', profile_list, name='list'),
    path('user=<slug:username>/', get_profile_by_username, name='get_by_username'),
    path('modify/<slug:username>/', update_delete_profile, name='update_delete')
]

urlpatterns = format_suffix_patterns(urlpatterns)
