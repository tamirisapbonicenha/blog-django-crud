from django import forms

from .models import Post, Author

class PostForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    category = forms.CharField()
    title = forms.CharField()
    text = forms.CharField()


class PostEdit(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'category') 
    
