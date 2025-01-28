from django import forms
from .models import Photo  # Photoモデルが存在している前提

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'description', 'is_downloadable'] 