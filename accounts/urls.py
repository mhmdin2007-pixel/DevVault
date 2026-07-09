from django.urls import path
from .views import RegisterView, CustomLoginview, CustomLogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginview.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]