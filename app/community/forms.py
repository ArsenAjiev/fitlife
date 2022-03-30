from django import forms
from community.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'tags']
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            # важно при загрузке изображения!!!
            'image': forms.FileInput(attrs={'class': 'input-image-control'})
        }
