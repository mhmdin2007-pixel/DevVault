from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Like, Comment, Vote, Bookmark, Follow, Answer
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from .forms import CommentForm, AnswerForm
from posts.models import Post
from django.contrib.auth.models import User

@login_required
@require_POST
def like_toggle(request, content_type_id, object_id):
    """
    Toggle like on any content (post, answer, etc.).
    Use AJAX-friendly response.
    """
    content_type = get_object_or_404(ContentType, id=content_type_id)
    content_object = content_type.get_object_for_this_type(id=object_id)

    like, created = Like.objects.get_or_create(
        user = request.user,
        content_type=content_type,
        object_id=object_id
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    total_likes = Like.objects.filter(
        content_type=content_type,
        object_id=object_id
    ).count()

    # AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'liked': liked,
                'total_likes': total_likes,
            })
    
    if liked:
        messages.success(request, 'Post liked!')
    else:
        messages.info(request, 'Like removed.')
    
    return redirect('posts:post_detali', slug=content_object.slug)

@login_required
@require_POST
def add_comment(request, content_type_id, object_id):
    '''
    Add a comment to any content.
    Supports replies via parent_id parametr.
    '''

    content_type = get_object_or_404(ContentType, id=content_type_id)
    content_object = content_type.get_object_for_this_type(id = object_id)

    form = CommentForm(request.Post)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.content_type = content_type
        comment.object_id = object_id

        # Handle reply to a comment
        parent_id = request.POST.get('parent_id')
        if parent_id:
             parent = get_object_or_404(Comment, id=parent_id)
             comment.parent = parent

        comment.save()
        messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Invalid comment. Please try again.')

    return redirect('posts:post_detail', slug=content_object.slug)

@login_required
@require_POST
def vote_toggle(request, content_type_id, object_id):
    """
    Toggle vote (upvote/downvote) on any content.
    """

    content_type = get_object_or_404(ContentType, id=content_type_id)
    content_object = content_type.get_all_objects_for_this_type(id=object_id)

    vote_type = request.POST.get('vote_type')
    if vote_type not in ['1', '-1']:
        messages.error(request, "Invalid vote type.")
        return redirect('posts:post_detail', slug=content_object.slug)

    vote_type = int(vote_type)

    #Check if user already voted
    existing_vote = Vote.object.filter(
        user = request.user,
        content_type=content_type,
        object_id=object_id
    ).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            #remove vote if same type
            existing_vote.delete()
            messages.info(request, "Vote removed.")
        else:
            #Update vote type
            existing_vote.vote_type = vote_type
            existing_vote.save()
            messages.success(request, "Vote updated!")
    else:
        #Create new vote
        Vote.object.create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            vote_type=vote_type
        )
        messages.success(request, "Vote added!")

    return redirect('posts:post_detail', slug=content_object.slug)

@login_required
@require_POST
def bookmark_toggle(request, content_type_id, object_id):
    """ Toggle bookmark on any content."""

    content_type = get_object_or_404(request, id=content_type_id)
    content_object = content_type.get_object_for_this_type(id=object_id)    
    
    bookmark, created = Bookmark.object.get_or_create(
        user= request.user,
        content_type=content_type,
        object_id=object_id
    )

    if not created:
        bookmark.delete()
        messages.info(request, "Bookmark removed!")
    else:
        messages.success(request, "Bookmarked!")
    
    return redirect('posts:post_detail', slug=content_object.slug)

@login_required
@require_POST
def follow_toggle(request, user_id):
    """ Toggle follow an a user. """

    target_user = get_object_or_404(User, id=user_id)

    if request.user == target_user:
        messages.error(request, "You cannot follow yourself.")
        return redirect('accounts:profile', username=target_user.username)
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user,
    )

    if not created:
        follow.delete()
        messages.info(request, f'Unfollowed {target_user.username}.')
    else:
        messages.success(request, f"Following {target_user.username}!")
    
    return redirect('accounts:profile', username=target_user.username)

@login_required
def answer_create(request, post_slug):
    """ Create an answer for an interview question with file upload. """
    post = get_object_or_404(Post, slug=post_slug)

    if not post.is_interview:
        messages.error(request, "This post does not accept answers.")
        return redirect('posts:post_detail', slug=post.slug)

    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_vaild():
            answer = form.save(commit=False)
            answer.post = post
            answer.author = request.user
            answer.save()
            messages.success(request, "Your answer has been submited!")

            return redirect('posts:post_detail', slug=post.slug)
        else:
            form = AnswerForm()
        
        context = {
            'form': form,
            'post': post,
        }

        return render(request, 'interactions/answer_form.html', context)
    
@login_required
@require_POST
def accept_answer(request, answer_id):
    '''
    Accept an answer for a post.
    Only the post author can accept an answer.
    '''

    answer = get_object_or_404(Answer, id=answer_id)
    post = answer.post

    #check if user is the post author
    if request.user != post.author:
        messages.error(request, "Only the post atuthor can accept answers.")
        return redirect('posts:post_detail', slug=post.slug)

    #toggle accepted status
    if answer.is_accepted:
        answer.is_accepted = False
        messages.info(request, "Answer unaccepted!")
    else:
        #Unaccept all other answers for this post
        Answer.objects.filter(post=post).update(is_accepted=False)
        answer.is_accepted = True
        messages.success(request, "Answer accepted!")

    answer.save()
    return redirect('posts:post_detail', slug=post.slug)
    