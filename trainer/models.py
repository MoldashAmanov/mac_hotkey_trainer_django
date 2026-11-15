from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField('Название урока', max_length=120)
    slug = models.SlugField('URL', max_length=120, unique=True)
    description = models.TextField('Описание', blank=True)
    icon = models.CharField('Иконка', max_length=10, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_published = models.BooleanField('Опубликован', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс',
    )
    title = models.CharField('Название урока', max_length=160)
    slug = models.SlugField('URL', max_length=160)
    description = models.TextField('Описание', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['course__order', 'order', 'title']
        unique_together = [('course', 'slug')]

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Hotkey(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='hotkeys',
        verbose_name='Урок',
    )
    action = models.CharField('Действие', max_length=200)
    keys = models.CharField('Сочетание клавиш', max_length=100)
    explanation = models.TextField('Объяснение', blank=True)
    difficulty = models.PositiveSmallIntegerField(
        'Сложность',
        default=1,
        choices=[
            (1, 'Легкая'),
            (2, 'Средняя'),
            (3, 'Сложная'),
        ],
    )
    is_active = models.BooleanField('Активна', default=True)
    physical = models.BooleanField(
        'Доступна для физической тренировки',
        default=True,
        help_text='Отключите для системных сочетаний, которые перехватывает macOS',
    )

    class Meta:
        verbose_name = 'Горячая клавиша'
        verbose_name_plural = 'Горячие клавиши'
        ordering = ['lesson__order', 'id']

    def __str__(self):
        return f'{self.action}: {self.keys}'


class UserProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hotkey_progress',
        verbose_name='Пользователь',
    )
    hotkey = models.ForeignKey(
        Hotkey,
        on_delete=models.CASCADE,
        related_name='user_progress',
        verbose_name='Горячая клавиша',
    )
    correct_answers = models.PositiveIntegerField('Правильных ответов', default=0)
    wrong_answers = models.PositiveIntegerField('Неправильных ответов', default=0)
    last_answered_at = models.DateTimeField('Последний ответ', auto_now=True)

    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'
        unique_together = [('user'), ('hotkey')]

    @property
    def accuracy(self):
        total = self.correct_answers + self.wrong_answers
        return round(self.correct_answers / total * 100) if total else 0

    def __str__(self):
        return f'{self.user} - {self.hotkey}'

    