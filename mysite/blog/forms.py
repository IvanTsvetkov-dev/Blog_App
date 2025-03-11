from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={"class": "form-control mb-2"}), label="Ваше имя")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control mb-2"}))
    to = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control mb-2"}), label="Email получателя")
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control mb-2"}), label="Комментарий")
    
    
class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2'}),
            'body': forms.Textarea(attrs={'class': 'form-control mb-2 '})
        }