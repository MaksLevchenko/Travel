from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Comment


class SigUpForm(forms.Form):
    """Форма регистрации"""
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
            'placeholder': "Введите логин."
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "inputPassword",
            'placeholder': "Введите пароль."
        })
    )

    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "inputPassword",
            'placeholder': "Повторите пароль."
        })
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                'Пароли не совпадают!'
            )

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class SignInForm(forms.Form):
    """Форма авторизации"""
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
            'placeholder': "Введите логин."
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "inputPassword",
            'placeholder': "Введите пароль."
        })
    )


class FeedBackForm(forms.Form):
    """Форма обратной связи"""
    name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "name",
            'placeholder': "Введите Ваше имя:"
        })
    )

    email = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': "form-control",
            'id': "email",
            'placeholder': "Введите Ваш email:"
        })
    )

    subject = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "subject",
            'placeholder': "Тема:"
        })
    )

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': "form-control md-textarea",
            'id': "message",
            'rows': 2,
            'placeholder': "Ваше сообщение:"
        })
    )


class CommentForm(forms.ModelForm):
    """Форма комментария"""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
