from django import forms

from .models import Post, Author

# class PostForm(forms.ModelForm):

#     class Meta:
#         model = Post
#         fields = ('title', 'text', 'author', 'category')

class PostForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    title = forms.CharField()
    text = forms.CharField()
    category = forms.CharField()


class PostEdit(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'category') 


class CategoryForm(forms.Form):
    name = forms.CharField()

    # def clean_name(self):
    #     if self.cleaned_data['name'] == 'Teste':
    #         raise forms.ValidationError(u'Digite um nome melhor.')
    #     else:
    #         return self.cleaned_data['name']    
