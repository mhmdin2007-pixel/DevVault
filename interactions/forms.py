from django import forms
from .models import Comment, Answer

class CommentForm():
    """
    From for adding comments with optional reply.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'row': 3,
                'placeholder': 'Write your comment...'
            }),
        }
        labels = {
            'content': 'Comment',
        }

class AnswerForm():
    """ Form for answering interview questions with file upload. """

    class Meta:
        model = Answer
        fields = ['content', 'solution_file', 'solution_note']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'row': 6,
                'placeholder': 'Write your answer...' 
            }),
            'solution_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes about your solution...'
            }),
            'solution_file': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'content': 'Answer',
            'solution_file': 'Upload Solution File',
            'solution_note': 'Additional Notes',
        }
        help_texts = {
            'solution_file': 'Upload your solution (main.cpp, solution.py, etc.)',
        }