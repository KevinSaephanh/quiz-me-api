from rest_framework.routers import DefaultRouter

from .views import CreateQuizView, VoteViewSet, CategoryViewSet, get_quizzes_by_category, quiz_list, RetrieveQuizByIdView, RetrieveQuizByTitleView, UpdateDestroyQuizView
from django.urls import path

router = DefaultRouter()
router.register(r'votes', VoteViewSet, basename='votes')
router.register(r'categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('quizzes/category/<slug:category_name>/<int:page>/',
         get_quizzes_by_category, name='list'),
    path('quizzes/page=<int:page>/', quiz_list, name='quiz_list'),
    path('quizzes/create/', CreateQuizView.as_view(), name='create'),
    path('quizzes/modify/<int:pk>/',
         UpdateDestroyQuizView.as_view(), name='modify'),
    path('quizzes/<int:pk>/', RetrieveQuizByIdView.as_view(), name='get_by_pk'),
    path('quizzes/get_by_title/',
         RetrieveQuizByTitleView.as_view(), name='get_by_title')
]
urlpatterns += router.urls
