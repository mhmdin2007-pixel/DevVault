from django.contrib import admin
from .models import Tag, Company, Post
from interactions.models import Answer


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'website']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


class AnswerInline(admin.TabularInline):
    """Display answers in the post admin page."""
    model = Answer
    extra = 1
    fields = ['author', 'content', 'is_accepted', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'post_type', 'category',
        'difficulty', 'company', 'created_at'
    ]
    list_filter = ['post_type', 'category', 'difficulty', 'company', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AnswerInline]
    filter_horizontal = ['tags']