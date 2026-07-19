from django.urls import path
from . import views

app_name = "interactions"

urlpatterns = [
    path('like/<int:content_type_id>/<int:object_id>/', views.like_toggle, name='like_toggle'),
    path('comment/<int:content_type_id>/<int:object_id>/', views.add_comment, name='add_comment'),
    path('vote/<int:content_type_id>/<int:object_id>/', views.vote_toggle, name='vote_toggle'),
    path('bookmark/<int:content_type_id>/<int:object_id>/', views.bookmark_toggle, name='bookmark_toggle'),
    path('follow/<int:user_id>/', views.follow_toggle, name='follow_toggle'),    path('answer/<slug:post_slug>/', views.answer_create, name='answer_create'),
    path('answer/accept/<int:answer_id>/', views.accept_answer, name='accept_answer'),
]