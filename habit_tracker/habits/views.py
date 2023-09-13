import base64
from datetime import date
import io

import matplotlib
import matplotlib.pyplot as plt

from django.db import models
from django.shortcuts import get_object_or_404, redirect, render

from .forms import HabitDetailForm, HabitForm
from .models import DailyHabit, Habit

matplotlib.use('Agg')


def index(request):
    current_date = str(date.today())
    habits = DailyHabit.objects.filter(date=current_date,
                                       habit__author=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.author = request.user
            habit.save()
            daily_habit = DailyHabit.objects.create(habit=habit)
            daily_habit.save()
            return redirect('habits:index')
    else:
        form = HabitForm()
    context = {
        'form': form,
        'habits': habits,
        'current_date': current_date,
    }
    return render(request, 'index.html', context)


def complete_habit(request, habit_id):
    habit = DailyHabit.objects.get(id=habit_id, habit__author=request.user)
    if request.method == 'POST':
        habit.completed = not habit.completed
        habit.save()
    return redirect('habits:index')


def habit_list(request, date):
    habit_date = date
    habits = DailyHabit.objects.filter(date=habit_date,
                                       habit__author=request.user)
    context = {
        'habits': habits,
        'habit_date': habit_date
    }
    return render(request, 'habit-list.html', context)


def habit_detail(request, habit_id):
    habit = get_object_or_404(
        Habit.objects.select_related('author'), pk=habit_id)
    form = HabitDetailForm(request.POST or None, instance=habit)
    context = {
        'habit': habit,
        'form': form
    }
    return render(request, 'habit-detail.html', context)


def habit_edit(request, habit_id):
    habit = get_object_or_404(Habit.objects.select_related('author'),
                              pk=habit_id)
    if habit.author == request.user:
        form = HabitForm(request.POST or None,
                         instance=habit)
        if form.is_valid():
            form.save()
            return redirect('habits:habit-detail', habit.id)
        return render(request, 'index.html', {'form': form})
    return redirect('habits:habit-detail', habit.id)


def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id)
    if habit.author == request.user:
        habit.delete()
        return redirect('habits:index')
    return redirect('habits:index')


def habit_chart(request):
    habits = DailyHabit.objects.filter(habit__author=request.user)
    # Находим количество выполненных привычек для
    #  каждого дня только для текущего пользователя
    completion_data = (habits.values('date')
                       .annotate(total_completed=models.Count(
                           'id', filter=models.Q(completed=True)
                        ))
                       .order_by('date'))
    # Создаем списки с данными для построения графика
    dates = [item['date'].strftime('%Y-%m-%d') for item in completion_data]
    completed = [item['total_completed'] for item in completion_data]
    # Создаем график
    fig, ax = plt.subplots()
    ax.plot(dates, completed)
    # Настройка осей x и y
    ax.set_xlabel('Дата')
    ax.set_ylabel('Количество выполненных привычек')
    # Поворот значений на оси x для лучшей читаемости
    plt.xticks(rotation=0)
    # Задаем значения оси y
    plt.yticks(range(0, Habit.objects.select_related('author').count() + 1))
    # Добавляем отметки с количеством выполненных
    # привычек только для текущего пользователя
    for i in range(len(dates)):
        completed_habits_count = habits.filter(date=dates[i],
                                               completed=True).count()
        if completed_habits_count > 0:
            ax.annotate(str(completed_habits_count),
                        (dates[i], completed_habits_count),
                        ha='center', va='bottom')
    # Конвертируем график в изображение
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = buffer.getvalue()
    buffer.close()
    # Кодируем изображение и передаем его в контекст шаблона
    image_base64 = base64.b64encode(image).decode('utf-8')
    context = {
        'image': image_base64
    }
    # Возвращаем шаблон с контекстом
    return render(request, 'habit-chart.html', context)
