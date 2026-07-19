from django.urls import path
from .views import RegisterView, CustomLoginview, CustomLogoutView, ProfileView, ProfileEditView
from django.contrib.auth.views import LogoutView
app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginview.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='posts:home'), name='logout'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
]