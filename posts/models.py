from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# from django.db.models import CheckConstraint, F, Q


class Tag(models.Model):
    '''
    Tag model for categorizing posts.
    Each tag has a unique name and slug.
    '''
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def save(self, *args, **kwargs):
        '''Auto-generate slug from name if not provided'''
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Company(models.Model):
    '''
    Company model for interview questions context.
    e.g., Google, Amazon, Snapp, Digikala..
    '''
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to='companies/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def save(self, *args, **kwargs):
        '''Auto-generate slug from name if not provided.'''
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    '''
    Main content model for DevVault.
    Represents interview questions, algorithm challenges, and teachnical posts.
    '''

    # you can view all of the following items in one place.
    # it is desplayed using dropdown menus in the admin panel.
    class Category(models.TextChoices):
        '''Available categories for posts.'''
        INTERVIEW = 'INTERVIEW', 'Interview' # interview question        
        ALGORITHM = 'ALGORITHM', 'Algorithm' # algorithm question
        SYSTEM_DESIGN = 'SYSTEM_DESIGN', 'System Design'
        SQL = 'SQL', 'SQL' # sql questions
        BACKEND = 'BACKEND', 'backend' # backend question
        LINUX = 'LINUX', 'linux' # linux questions

    class Difficulty(models.TextChoices):
        '''Difficulty levels for posts.'''
        BEGINNER = 'BEGINNER', 'Beginner'
        INTERMEDIATE = 'INTERMEDIATE', 'Intermediate'
        ADVANCED = 'ADVANCED', 'Advanced'

    #fields
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Author')
    title = models.CharField(max_length=200, verbose_name='Title')
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name='Slug'
    )
    content = models.TextField(verbose_name='Content')
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.INTERVIEW,
        verbose_name='Category'
    )
    difficulty = models.CharField(
        max_length=20, 
        choices=Difficulty.choices,
        default=Difficulty.BEGINNER,
        verbose_name='Difficulty'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Company'
    )
    tags = models.ManyToManyField(
        Tag, 
        related_name='posts',
        blank=True, 
        verbose_name='Tags'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = [
            # index for fast search
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['category', 'difficulty']),
        ]
    
    def save(self, *args, **kwargs):
        '''
        Override save to auto-generate slug from title.
        '''
        if not self.slug:
            base_slug = slugify(self.title)

            # if sulg is duplicate (unique=True) add a number to it.
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        ''' Return title as string representation.'''
        return self.title
    
    @property
    def votes_count(self):
        '''
        Calculate total votes for this post.
        '''
        from django.db.models import Sum
        result = self.votes.aggregate(total=Sum('vote_type'))['total']
        return result or 0
    
    @property
    def answers_count(self):
        return self.answers.count()

    @property
    def is_answered(self):
        """Check if post has an accepted answer."""
        return self.answers.filter(is_accepted=True).exists()
    
    def accepted_answer(self):
        """Return the accepted answer if exists."""
        return self.answers.filter(is_accepted=True).first()

class Answer(models.Model):
    '''
    Answer model for posts.
    Each answer belongs to a post and a user.
    Only one answer per post can be accepted.
    '''
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Post'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Author'
    )
    content = models.TextField(verbose_name='Content')
    is_accepted = models.BooleanField(
        default=False,
        verbose_name='Is Accepted'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

        constraints = [
            models.UniqueConstraint(
                fields=['post'],
                condition=models.Q(is_accepted=True),
                name='unique_accepted_answer'
            )
        ]
    
    def save(self, *args, **kwargs):
        '''
            Override save to handle accepted answer logic.
        '''
        if self.is_accepted:
            Answer.objects.filter(post=self.post).exclude(id=self.id).update(is_accepted=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Answer by {self.author.username} on {self.post.title[:30]}"
    
class Vote(models.Model):
    '''
    Vote model for posts.
    Each user can vote once per post (upvote or downvote).
    '''
    class VoteType(models.IntegerChoices):
        DOWNVOTE = -1, 'Downvote'
        UPVOTE = 1, 'Upvote'
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='User'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='Post'
    )
    vote_type = models.IntegerField(
        choices=VoteType.choices,
        verbose_name='Vote Type'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now = True,
        verbose_name='Updated At'
    )

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

        # هر کاربر فقط یک بار میتونه به هر پست رای بده.
        unique_together = ['user', 'post']
        indexes = [
            models.Index(fields=['user', 'post'])
        ]

    def __str__(self):
        return f"{self.user.username} {self.get_vote_type_display()} on {self.post.title[:30]}"
    

class Bookmark(models.Model):
    '''
    Bookmark model for saving favorite posts.
    Each user can bookmark multiple posts.
    '''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='User' 
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='Post'
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    
    class Meta:
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'
        # هر کاربر فقط یکبار میتونه هر پست را سیو کنه
        unique_together = ['user', 'post']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title[:30]}"
    
class Follow(models.Model):
    '''
    Follow model for user-to-user relationships.
    A user can follow another user.
    '''
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Following'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        # هر کاربر نمیتونه دوبار یه نفر رو فالو کنه
        unique_together = ['follower', 'following']
        # این قسمت رو باید توی views چک کنیم  که کاربر نمیتونه خودش رو هم فالو کنه
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(follower=models.F('following')),
                name='cannot_follow_self'
            )
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"