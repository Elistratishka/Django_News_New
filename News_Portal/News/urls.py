from django.urls import path
from .views import PostList, PostView, PostSearch, PostAdd, PostEdit, PostDelete


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostView.as_view(), name='detail'),
    path('<int:pk>/edit', PostEdit.as_view(), name='edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='delete'),
    path('search', PostSearch.as_view(), name='search'),
    path('add', PostAdd.as_view(), name='add')
]
