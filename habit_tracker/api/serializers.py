from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Habit
        fields = '__all__'
