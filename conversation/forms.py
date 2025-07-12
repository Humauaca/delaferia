from django import forms
from . import models

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = models.ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }