from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].empty_label = "Если хотите, выберите группу"
        self.fields['group'].required = False

    class Meta:
        model = Post
        fields = ['text', 'group']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 40, 'rows': 10})
        }
