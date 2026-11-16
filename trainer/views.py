import json
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView

from .forms import CourseForm, HotkeyForm, LessonForm, SignUpForm
from .keymap import parse_macos_keys
from .models import Course, Lesson
from .services import (
    build_training_set,
    get_course_with_lessons,
    get_published_courses,
    get_user_stats,
    save_answer,
)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('trainer:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def home(request):
    courses = get_published_courses()
    stats = get_user_stats(request.user) if request.user.is_authenticated else None

    return render(
        request,
        'trainer/home.html',
        {'courses': courses, 'stats': stats}
    )


def course_detail(request, course_slug):
    course = get_course_with_lessons(course_slug)

    if course is None:
        return render(request, 'trainer/404.html', status=404)

    return render(request, 'trainer/course_detail.html', {'course': course})


def lesson_detail(request, course_slug, lesson_slug):
    lesson = get_object_or_404(
        Lesson,
        slug=lesson_slug,
        course__slug=course_slug,
        course__is_published=True,
    )

    return render(
        request,
        'trainer/lesson_detail.html',
        {
            'lesson': lesson,
            'hotkeys': lesson.hotkeys.filter(is_active=True),
        },
    )


@login_required
def training(request, course_slug, lesson_slug):
    lesson = get_object_or_404(
        Lesson,
        slug=lesson_slug,
        course__slug=course_slug,
    )

    items = build_training_set(request.user, course_slug, lesson_slug)

    return render(
        request,
        'trainer/training.html',
        {'items':items, 'lesson': lesson},
    )


@login_required
def physical_training(request, course_slug, lesson_slug):
    lesson = get_object_or_404(
        Lesson,
        slug=lesson_slug,
        course__slug=course_slug,
    )

    items = build_training_set(
        request.user,
        course_slug,
        lesson_slug,
        physical_only=True,
    )

    for item in items:
        parsed = parse_macos_keys(item['keys'])
        item['modifiers'] = parsed['modifiers']
        item['main_key'] = parsed['main_key']

    return render(
        request,
        'trainer/physical_training.html',
        {'items': items, 'lesson': lesson},
    )

@login_required
@require_POST
def api_check_answer(request):
    try:
        data = json.loads(request.body)
        hotkey_id = int(data['hotkey_id'])
        selected = str(data['selected'])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Некорректный запрос'}, status=400)

    try:
        hotkey = Lesson.hotkeys.field.model.object.get(
            pk=hotkey_id,
            is_active=True,
        )
    except Lesson.hotkeys.field.model.DoesNotExist:
        return JsonResponse({'error': 'Горячая клавиша не найдена'}, status=400)

    is_correct = selected == hotkey.keys
    progress = save_answer(request.user, hotkey_id, is_correct)

    return JsonResponse(
        {
            'correct': is_correct,
            'correct_answer': progress.correct_answers,
            'wrong_answer': progress.wrong_answers,
            'accuracy': progress.accuracy,
        }
    )


@login_required
def profile(request):
    return render(
        request,
        'trainer/profile.html',
        {'stats': get_user_stats(request.user)},
    )


@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('trainer:home')
    else:
        form = CourseForm()

    return render(request, 'trainer/course_form.html', {'form': form})


@login_required
def create_lesson(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    if request.method == 'POST':
        form = LessonForm(request.POST)

        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('trainer:course_detail', course_slug=course.slug)
    else:
        form = LessonForm()

    return render(
        request,
        'trainer/lesson_form.html',
        {'form': form, 'course': course},
    )


@login_required
def create_hotkey(request, course_slug, lesson_slug):
    lesson = get_object_or_404(
        Lesson,
        slug=lesson_slug,
        course__slug=course_slug,
    )

    if request.method == 'POST':
        form = HotkeyForm(request.POST)

        if form.is_valid():
            hotkey = form.save(commit=False)
            hotkey.lesson = lesson
            hotkey.save()
            return redirect('trainer:lesson_detail', course_slug, lesson_slug)
    else:
        form = HotkeyForm()

    return render(
        request,
        'trainer/hotkey_form.html',
        {'form': form, 'lesson': lesson},
    )
