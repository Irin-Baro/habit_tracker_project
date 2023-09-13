from django.urls import path

from . import views

app_name = 'habits'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'complete-habit/<int:habit_id>/',
        views.complete_habit,
        name='complete-habit'
    ),
    path(
        'habit-chart/',
        views.habit_chart,
        name='habit-chart'
    ),
    path(
        'habits/<int:habit_id>/detail/',
        views.habit_detail,
        name='habit-detail'
    ),
    path(
        'habits/<int:habit_id>/edit/',
        views.habit_edit, name='habit-edit'
    ),
    path(
        'habits/<int:habit_id>/delete/',
        views.habit_delete,
        name='habit-delete'
    ),
    path(
        'daily-habits/<str:date>/',
        views.habit_list,
        name='daily-habits'
    ),
]
