from django.db.models import Count, F, Sum

from .models import Course, Hotkey, UserProgress


def get_published_courses():
    return Course.objects.filter(is_published=True)


def get_course_with_lessons(slug):
    return (
        Course.objects
        .prefetch_related('lessons')
        .filter(slug=slug, is_published=True)
        .first()
    )


def get_lesson_hotkeys(course_slug, lesson_slug):
    return Hotkey.objects.filter(
        lesson__slug=lesson_slug,
        lesson__course__slug=course_slug,
        lesson__course__is_published=True,
        is_active=True,
    )


def build_training_set(user, course_slug, lesson_slug, limit=10, physical_only=False):
    queryset = get_lesson_hotkeys(course_slug, lesson_slug)

    if physical_only:
        queryset = queryset.filter(physical=True)

    queryset = queryset.order_by('?')[:limit]

    progress_map = {
        progress.hotkey_id: progress
        for progress in UserProgress.objects.filter(
            user=user,
            hotkey__in=queryset,
        )
    }

    return [
        {
            'id': hotkey.id,
            'action': hotkey.action,
            'keys': hotkey.keys,
            'difficulty': hotkey.difficulty,
            'correct': progress_map[hotkey.id].correct_answers if hotkey.id in progress_map else 0,
            'wrong': progress_map[hotkey.id].wrong_answers if hotkey.id in progress_map else 0,
        }
        for hotkey in queryset
    ]


def save_answer(user, hotkey_id, is_correct):
    try:
        hotkey = Hotkey.objects.get(pk=hotkey_id, is_active=True)
    except Hotkey.DoesNotExist:
        return None

    progress, _ = UserProgress.objects.get_or_create(
        user=user,
        hotkey=hotkey,
    )

    if is_correct:
        progress.correct_answers = F('correct_answers') + 1
    else:
        progress.wrong_answers = F('wrong_answers') + 1

    progress.save()
    progress.refresh_from_db()
    return progress


def get_user_stats(user):
    data = UserProgress.objects.filter(user=user).aggregate(
        learned=Count('id'),
        correct=Sum('correct_answers'),
        wrong=Sum('wrong_answers'),
    )

    correct = data['correct'] or 0
    wrong = data['wrong'] or 0
    total = correct + wrong

    return {
        'learned_hotkeys': data['learned'],
        'total_correct': correct,
        'total_wrong': wrong,
        'accuracy': round(correct / total * 100) if total else 0,
    }