from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    LeadTimeValidator,
    PeriodicityValidator,
    AssociatedHabitOrRewardValidator,
    PleasurableHabitValidator,
    AssociatedHabitIsPleasurableHabitValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            "id",
            "place",
            "time",
            "periodicity",
            "action",
            "is_pleasurable",
            "associated_habit",
            "reward",
            "lead_time",
            "is_public",
        )
        validators = [
            LeadTimeValidator(field="lead_time"),
            PeriodicityValidator(field="periodicity"),
            AssociatedHabitOrRewardValidator(field="reward"),
            PleasurableHabitValidator(field="associated_habit"),
            PleasurableHabitValidator(field="reward"),
            AssociatedHabitIsPleasurableHabitValidator(field="associated_habit"),
        ]


class HabitPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            "place",
            "time",
            "periodicity",
            "action",
            "is_pleasurable",
            "associated_habit",
            "reward",
            "lead_time",
        )
