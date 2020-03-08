from rest_framework.routers import DefaultRouter

from .views import VoteViewSet, CategoryViewSet, get_quizzes_by_category, create_quiz, get_quiz, quiz_list, update_delete_quiz
from django.urls import path

router = DefaultRouter()
router.register(r'votes', VoteViewSet, basename='votes')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('quizzes/category/<slug:category_name>/<int:page>/',
         get_quizzes_by_category, name='list'),
    path('quizzes/<int:page>/', quiz_list, name='quiz_list'),
    path('quizzes/', create_quiz, name='post_qgiuiz'),
    path('quizzes/quiz=<int:pk>/', get_quiz, name='get_quiz'),
    path('quizzes/modify/<int:pk>/', update_delete_quiz, name='modify'),
]
urlpatterns += router.urls
