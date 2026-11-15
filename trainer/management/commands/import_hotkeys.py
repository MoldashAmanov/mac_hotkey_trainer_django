from django.core.management.base import BaseCommand

from trainer.data.macos_hotkeys import MACOS_HOTKEYS
from trainer.models import Course, Hotkey, Lesson


class Command(BaseCommand):
    help = 'Импортирует курсы, уроки и горячие клавиши macOS'

    def handle(self, *args, **options):
        courses = lessons = hotkeys = 0

        for item in MACOS_HOTKEYS:
            course_data = item['course']
            course, created = Course.objects.update_or_create(
                slug=course_data['slug'],
                defaults={
                    'title': course_data['title'],
                    'description': course_data['description'],
                    'icon': course_data['icon'],
                    'order': course_data['order'],
                    'is_published': True,
                },
            )
            courses += int(created)

            for lesson_data in item['lessons']:
                lesson, created = Lesson.objects.update_or_create(
                    course=course,
                    slug=lesson_data['slug'],
                    defaults={
                        'title': lesson_data['title'],
                        'description': lesson_data['description'],
                        'order': lesson_data['order'],
                    },
                )
                lessons += int(created)

                for hotkey_data in lesson_data['hotkeys']:
                    _, created = Hotkey.objects.update_or_create(
                        lesson=lesson,
                        action=hotkey_data['action'],
                        defaults={
                            'keys': hotkey_data['keys'],
                            'explanation': hotkey_data['explanation'],
                            'difficulty': hotkey_data['difficulty'],
                            'physical': hotkey_data.get('physical', True),
                            'is_active': True,
                        },
                    )
                    hotkeys += int(created)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Импортировано: курсов {courses}, уроков {lessons}, клавиш {hotkeys}'
            )
        )
