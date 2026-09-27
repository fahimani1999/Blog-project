from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter blog title'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your blog content...',
                'rows': 8
            }),
        }