from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    '''Inline editing for profile within User admin.'''
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"

class CustomUserAdmin(UserAdmin):
    '''Custom User admin with Profile inline.'''
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# admin.site.register(User)
# admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''profile admin configuration.'''
    list_display = ('user', 'full_name', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio')
    list_filter = ('created_at', )
    readonly_fields = ('created_at', 'updated_at')

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = "Full Name"
    