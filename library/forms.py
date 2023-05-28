
from django import forms
from django.contrib.auth.forms import UserCreationForm

from library.models import User, IssuedDocument, Message, Book, Category


class IssuedDocumentForm(forms.ModelForm):
    class Meta:
        model = IssuedDocument
        fields = ['name', 'date_issued', 'date_give',
                  'name_of_reader', 'number_read_bilet']


class BookFilterForm(forms.Form):
    name = forms.CharField(required=False)
    author = forms.CharField(required=False)
    izdat = forms.CharField(required=False)
    category = forms.CharField(required=False)
    invented_number = forms.IntegerField(required=False)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField
    # birth_of_date = forms.DateField

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'birth_of_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),

        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
