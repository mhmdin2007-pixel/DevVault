from django.contrib import admin
from .models import Tag, Company, Answer, Post, Vote, Bookmark, Follow

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'website']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name', )}
    readonly_fields = ['created_at', 'updated_at']

class AnswerInline(admin.TabularInline):
    '''display the answers in post page.'''
    model = Answer
    extra = 1
    fields = ['author', 'content', 'is_accepted', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'difficulty', 'company', 'created_at']
    list_filter = ['category', 'difficulty', 'company', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title', )}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AnswerInline]
    filter_horizontal = ['tags']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'is_accepted', 'created_at']
    list_filter = ['is_accepted', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Bookmark)
class BookmardAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    search_fields = ['user__username', 'post__title']
    readonly_fields = ['created_at']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__usernmae', 'following__username']
    readonly_fields = ['created_at']

