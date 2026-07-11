from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    Form for creating and editing posts.
    Dynamically updates fields based on post type.
    """

    class Meta:
        model = Post
        fields = [
            'post_type', 'title', 'content', 'image', 'video', 'summary',
            'category', 'difficulty', 'company', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'row': 10,
                'placeholder': 'Write your post content here...'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief summary of your post...'
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-select'
            }),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'post_type': 'Post Type',
            'title': 'Title',
            'content': 'Content',
            'image': 'Image (optional)',
            'video': "Video (optional)",
            'summary': 'Summary (optional)',
            'category': 'Category (for interview posts)',
            'difficulty': "Difficulty (for interview posts)",
            'company': 'Comoany (optional)',
            'tags': 'Tags (optional)',
        }

        help_text = {
            'tags': 'Hold Ctrl to select multiple tags',
            'image': 'Upload a cover image for your post',
            'video': 'Updoad a video file (mp4, webm, etc.)',
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # make interview fields optional by default
            self.fields['category'].required = False
            self.fields['difficulty'].required = False
            self.fields['company'].required = False
            self.fields['tags'].required = False
            self.fields['image'].required = False
            self.fields['video'].required = False
            self.fields['summary'].required = False