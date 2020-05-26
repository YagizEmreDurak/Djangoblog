from django import forms
from .models import article

class articleform(forms.ModelForm):
    class Meta:
        model = article
        fields = ["title" , "content" , "article_image"]
