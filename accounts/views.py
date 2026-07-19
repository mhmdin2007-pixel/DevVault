from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView#ویو های آماده جنگو برای ورود و خروج
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile

class ProfileView(DetailView):
    '''Display user profile with thier posts and stats.'''
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        '''Get user by username from URL.'''
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        context['user_posts'] = user.posts.all()[:10]

        return context
    
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Editing user profile."""
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'

    def get_object(self):
        """Get the profile of the current user."""
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        return profile
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    
    def get_success_url(self):
        messages.success(self.request, "پروفایل شما با موفقیت ویرایش شد.")
        return reverse_lazy('accounts:profile', kwargs={
            'username': self.request.user.username
        })
    
    def form_valid(self, form):
        messages.success(self.request, "پروفایل شما با موفقیت ویرایش شد.")
        return super().form_valid(form)

class RegisterView(CreateView, LoginRequiredMixin):
    '''User registeration with automatic login after signup.'''
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('posts:home')

    def form_valid(self, form):
        '''Login the user after successful registration.'''
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f"{self.object.username}! Your account has been created.")
        return response

    def dispatch(self, request, *args, **kwargs):
        '''Redirect authenticated users to home page.'''
        if request.user.is_authenticated:
            return redirect('posts:home')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginview(LoginView):
    '''Custom login view with echanced messaging.'''
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        '''Add success messages on login.'''
        messages.success(self.request, f"Welcome back {self.request.user.username}!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        '''Add error message on failed login.'''
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)
    
class CustomLogoutView(LogoutView):
    '''Custom logout view with confiramation message.'''
    next_page = reverse_lazy('posts:home')

    def dispatch(self, request, *args, **kwargs):
        '''Add info message before logout.'''
        messages.info(request, "you have been succussfully loggedout.")
        return super().dispatch(request, *args, **kwargs)
    