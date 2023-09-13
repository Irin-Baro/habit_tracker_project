from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def create_habit_list_daily():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    from .models import Habit, DailyHabit
    users = User.objects.all()
    for user in users:
        habits = Habit.objects.filter(author=user)
        for habit in habits:
            date_today = datetime.today().date()
            daily_habit, created = DailyHabit.objects.get_or_create(
                habit=habit, date=date_today)
            if not created:
                print('DailyHabit object already exists')


scheduler = BackgroundScheduler()
scheduler.add_job(create_habit_list_daily, 'interval', days=1,
                  start_date='2023-09-14 00:00:00')
# 'interval', days=1)
scheduler.start()
