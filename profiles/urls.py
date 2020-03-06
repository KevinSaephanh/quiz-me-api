from .views import ProfileListView, ProfileCreateView, ProfileRetrieveUpdateDestroyView
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', ProfileListView.as_view()),
    path('<int:pk>', ProfileRetrieveUpdateDestroyView.as_view()),
    path('<slug:username>', ProfileCreateView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
