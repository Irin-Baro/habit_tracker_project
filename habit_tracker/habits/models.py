from datetime import date
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Habit(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Привычка',
        help_text='Укажите название привычки'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Автор',
    )
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return self.title


class DailyHabit(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='daily_habits',
        verbose_name='Привычка',
    )
    date = models.DateField(
        default=date.today,
        verbose_name='Дата'
    )
    completed = models.BooleanField(
        default=False,
        verbose_name='Выполнено'
    )

    class Meta:
        verbose_name = 'Ежедневная привычка'
        verbose_name_plural = 'Ежедневные привычки'

    def __str__(self):
        return f'{self.date}: {self.habit} - {self.completed}'
