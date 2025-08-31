# updates/forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'subtitle', 'category', 'body', 
            'featured_image', 'featured_video', 'attachment',
            'title_color', 'font_size', 'underline_title',
            'published_at', 'status'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'},format='%Y-%m-%dT%H:%M'),  # <-- Add this format argument
            'status': forms.Select(attrs={'class': 'form-select'}),
            'title_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'font_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'underline_title': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # CKEditor is automatically applied to the 'body' field
        }
