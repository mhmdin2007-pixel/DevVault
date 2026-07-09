from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView #ویو های آماده جنگو برای ورود و خروج
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(CreateView, LoginRequiredMixin):
    '''User registeration with automatic login after signup.'''
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('posts:home')

    def form_valid(self, form):
        '''Log the user after successful registration.'''
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