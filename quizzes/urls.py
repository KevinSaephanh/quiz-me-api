from rest_framework.routers import DefaultRouter

from .views import QuizViewSet, VoteViewSet, CategoryViewSet, get_quizzes_by_category
from django.urls import path

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quizzes')
router.register(r'votes', VoteViewSet, basename='votes')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('quizzes/category/<slug:category_name>/<int:page>/',
         get_quizzes_by_category, name='list')
]
urlpatterns += router.urls
