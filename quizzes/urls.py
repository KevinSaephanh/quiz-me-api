from rest_framework.routers import DefaultRouter

from .views import VoteViewSet, CategoryViewSet, get_quizzes_by_category, quiz_list, QuizViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'votes', VoteViewSet, basename='votes')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'quizzes', QuizViewSet, basename='quizzes')


urlpatterns = [
    path('quizzes/category/<slug:category_name>/<int:page>/',
         get_quizzes_by_category, name='list'),
    path('quizzes/page=<int:page>/', quiz_list, name='quiz_list'),
]
urlpatterns += router.urls
