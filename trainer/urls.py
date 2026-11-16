from django.urls import path

from . import views

app_name = 'trainer'

urlpatterns = [
    path('', views.home, hame='home'),
    path('courses/<slug:course_slug>/', views.course_detail, name='course_detail'),
    path(
        'courses/<slug:course_slug>/<slug:lesson_slug>/',
        views.lesson_detail,
        name='lesson_detail',
    ),
    path(
        'courses/<slug:course_slug>/<slug:lesson_slug>/training/',
        views.training,
        name='training',
    ),
    path(
        'courses/<slug:course_slug/<slug:lesson_slug>/physical-training/',
        views.physical_training,
        name='physical_training',
    ),
    path('api/check-answer/', views.api_check_answer, name='api_check_answer'),
    path('profile/', views.profile, name='profile'),
    path('courses/new/', views.create_course, name='create_course'),
    path(
        'courses/<slug:course_slug>/lessons/new/',
        views.create_lesson,
        name='create_lesson',
    ),
    path(
        'courses/<slug:course_slug>/<slug:lesson_slug>/hotkeys/new/',
        views.create_hotkey,
        name='create_hotkey',
    ),
]