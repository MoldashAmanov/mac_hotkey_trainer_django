from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Course, Hotkey, Lesson


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        help_text='Нужен для восстановления пароля',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'slug', 'description', 'icon', 'order', 'is_published']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'slug', 'description', 'order']


class HotkeyForm(forms.ModelForm):
    class Meta:
        model = Hotkey
        fields = ['action', 'keys', 'explanation', 'difficulty', 'is_active', 'physical']
        