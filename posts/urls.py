from .models import Tag
from django.urls import path

from .views import PostDetailView, PostListView

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]