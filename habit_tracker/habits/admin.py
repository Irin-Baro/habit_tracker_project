from django.contrib import admin

from .models import Habit, DailyHabit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created')


@admin.register(DailyHabit)
class DailyHabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit', 'habit_author', 'date', 'completed')
    list_filter = ('date', )
    search_fields = ('habit', 'habit_author',)
    date_hierarchy = 'date'

    def habit_author(self, obj):
        return obj.habit.author
    habit_author.short_description = 'Пользователь'
