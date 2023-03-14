from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view()),
    path('search/', NewsListFilt.as_view()),
    path('add/', PostCreateView.as_view()),
    path('<int:pk>/edit/', PostUpdateView.as_view()),
    path('<int:pk>/delete/', PostDeleteView.as_view()),
]
