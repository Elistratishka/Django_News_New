from django.urls import path
from .views import PostList, PostView


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostView.as_view()),
]
