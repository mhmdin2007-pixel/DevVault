from .models import Tag
from django.urls import path

from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]