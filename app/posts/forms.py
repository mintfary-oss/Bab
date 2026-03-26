from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = Post
        fields = ["title", "body", "visibility", "status", "pregnancy_week"]


class CommentForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Комментарий..."}
            )
        }
