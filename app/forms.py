from django import forms
from django.contrib.auth.models import User

from app.models import Profile, Question, Tag, Answer


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-lg', 'placeholder': 'Enter your username'}))
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(
        attrs={'class': 'form-control-lg', 'placeholder': 'Enter your password'}))

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == "wrongpass":
            raise forms.ValidationError("Wrong password")
        return data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput())
    password_check = forms.CharField(min_length=4, widget=forms.PasswordInput())
    avatar = forms.ImageField(label='Upload avatar', required=False,
                              widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')
        if password != password_check:
            raise forms.ValidationError("Passwords don't match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, avatar=self.cleaned_data.get('avatar'))
        return user


class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = User
        fields = ['email', 'username']

    def save(self, commit=True, **kwargs):
        user = super().save(**kwargs)
        if commit:
            user.save()
            if self.cleaned_data.get('avatar'):
                profile, created = Profile.objects.get_or_create(user=user)
                profile.avatar = self.cleaned_data['avatar']
                profile.save()
        return user


class QuestionForm(forms.ModelForm):
    title = forms.CharField(min_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(min_length=15, widget=forms.Textarea(attrs={'class': 'form-control'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
            self.save_tags(question)
        return question

    def save_tags(self, question):
        tags_input = self.cleaned_data.get('tags')
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(', ')]
            for tag_name in tag_names:
                print(tag_name)
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)


class AnswerForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your answer...'}),
        label=''
    )

    class Meta:
        model = Answer
        fields = ['text']
