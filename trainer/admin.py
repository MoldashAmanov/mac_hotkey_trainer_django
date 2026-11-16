from django.contrib import admin

from .models import Course, Hotkey, Lesson, UserProgress


class HotkeyInline(admin.TabularInline):
    model = Hotkey
    extra = 1
    fields = ('action', 'keys', 'explanation', 'difficulty', 'is_active', 'physical')


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'is_published', 'created_at')
    list_editable = ('order', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'destciption')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]


@admin.register(Hotkey)
class HotkeyAdmin(admin.ModelAdmin):
    list_display = ('action', 'keys', 'lesson', 'difficulty', 'is_active', 'physical')
    list_filter = ('lesson__course', 'difficulty', 'is_active', 'physical')
    search_fields = ('action', 'keys', 'explanation')
    list_editable = ('difficulty', 'is_active', 'physical')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotkey', 'correct_answers', 'wrong_answers', 'accuracy')
    search_fields = ('user__username', 'hotkey__action')

