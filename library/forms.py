from django import forms

from library.models import IssuedDocument, Message


class IssuedDocumentForm(forms.ModelForm):
    class Meta:
        model = IssuedDocument
        fields = '__all__'


class BookFilterForm(forms.Form):
    name = forms.CharField(required=False)
    author = forms.CharField(required=False)
    izdat = forms.CharField(required=False)
    category = forms.CharField(required=False)
    invented_number = forms.IntegerField(required=False)


class MessageSendForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['user', 'room', 'content']
