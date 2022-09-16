from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'categories',
            'title',
            'text',
            # 'post_type',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        if text == title:
            raise ValidationError(
                {'text': 'Текст публикации не должен быть идентичен её названию'}
            )
        return cleaned_data