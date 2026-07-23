from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Company, Tag
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# posts/views.py

class PostListView(ListView):
    """
    Display posts from followed users first.
    If not logged in or no followed users, show all posts.
    """
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        """Apply filters and search to the post queryset."""
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        
        #منطق پایه (فالو یا همه پست‌ها)
        if not search_query:
            if self.request.user.is_authenticated:
                followed_users = self.request.user.following.all().values_list('following', flat=True)
                if followed_users.exists():
                    queryset = Post.objects.filter(
                        Q(author__in=followed_users) | Q(author__isnull=False)
                    ).distinct().order_by('-created_at')
                else:
                    queryset = Post.objects.all().order_by('-created_at')
            else:
                queryset = Post.objects.all().order_by('-created_at')
        else:
            # اگر جستجو وجود داشته باشه، فالو نادیده گرفته میشه
            queryset = Post.objects.all().order_by('-created_at')
        
        #جستجو (اگه عبارت وجود داشته باشه)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            ).distinct()
        
        #فیلترها (post_type, category, difficulty, ...)
        post_type = self.request.GET.get('post_type')
        if post_type:
            queryset = queryset.filter(post_type=post_type)

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        company = self.request.GET.get('company')
        if company:
            queryset = queryset.filter(company__slug=company)

        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add filter options and current filters to context."""
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('q')
        
        # جستجوی کاربران
        if search_query:
            context['search_users'] = User.objects.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            ).distinct()[:10]
        else:
            context['search_users'] = None
        
        context['search_query'] = search_query
        
        #فیلترها
        context['categories'] = Post.Category.choices
        context['difficulties'] = Post.Difficulty.choices
        context['post_types'] = Post.PostType.choices
        context['companies'] = Company.objects.all()
        context['tags'] = Tag.objects.all()

        context['current_filters'] = {
            'post_type': self.request.GET.get('post_type', ''),
            'category': self.request.GET.get('category', ''),
            'difficulty': self.request.GET.get('difficulty', ''),
            'company': self.request.GET.get('company', ''),
            'tag': self.request.GET.get('tag', ''),
            'q': self.request.GET.get('q', ''),
        }

        #وضعیت فالو
        
        if self.request.user.is_authenticated:
            followed_users = self.request.user.following.all().values_list('following', flat=True)
            context['has_following'] = followed_users.exists()
        else:
            context['has_following'] = False

        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new post with any type(SOCILA, INTERVIEW, ARTICLE).
    User must be authenticated.
    """
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        '''Set author to current user before saving.'''
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={
            'slug': self.object.slug
        })

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    Update an existin post.
    Only the author can update.
    '''
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def test_func(self):
        """Check if current user is the author."""
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, "Your post has been updated successfully!")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={
            'slug': self.object.slug
        })
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''
    Delete a post.
    Only the author can delete.
    '''
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:home')

    def test_func(self):
        """Check if current user is the author."""
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your post has been deleted successfully!")
        return super().delete(request, *args, **kwargs)
    
class PostDetailView(DetailView):
    '''
    Display full post detail with comments and user interactions.
    '''
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_object(self):
        '''Get post by slug.'''
        return get_object_or_404(Post, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_type'] = ContentType.objects.get_for_model(Post)

        from interactions.models import Comment
        context['comments'] = Comment.objects.filter(
            content_type__model='post',
            object_id=self.object.id
        ).order_by('created_at')

        if self.request.user.is_authenticated:
            from interactions.models import Like, Vote, Bookmark
            content_type = ContentType.objects.get_for_model(Post)

            context['user_liked'] = Like.objects.filter(
                user=self.request.user,
                content_type=content_type,
                object_id=self.object.id
            ).exists()

            context['user_voted'] = Vote.objects.filter(
                user=self.request.user,
                content_type=content_type,
                object_id=self.object.id
            ).first()

            context['user_bookmarked'] = Bookmark.objects.filter(
                user=self.request.user,
                content_type=content_type,
                object_id=self.object.id
            ).exists()

        return context