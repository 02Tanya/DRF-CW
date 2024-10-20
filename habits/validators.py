from rest_framework.exceptions import ValidationError

from habits.models import Habit


class LeadTimeValidator:
    '''Проверка продолжительности выполнения привычки'''

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val > 120:
            raise ValidationError('Время выполнения привычки - не более 120 сек.')


class PeriodicityValidator:
    '''Проверка частоты выполнения привычки'''

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val > 7:
            raise ValidationError('Привычку надо выполнять не реже, чем 1 раз за 7 дней')


class AssociatedHabitOrRewardValidator:
    '''Проверяет, что вознаграждение и связанная привычка не пересекаются'''

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        associated_habit = dict(value).get('associated_habit')
        reward = dict(value).get(self.field)
        if associated_habit is not None and reward is not None:
            raise ValidationError('Нельзя назначать вознаграждение и связанную привычку вместе')


class PleasurableHabitValidator:
    '''Проверяет, что у приятной привычки не назначено вознаграждение или связанная привычка'''

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        is_pleasurable = dict(value).get('is_pleasurable')
        tmp_val = dict(value).get(self.field)
        if is_pleasurable and tmp_val is not None:
            raise ValidationError('Нельзя назначать вознаграждение или связанную привычку для приятной привычки')


class AssociatedHabitIsPleasurableHabitValidator:
    '''Проверяет, что связанная привычка является приятной'''

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        associated_habit = dict(value).get(self.field)
        if associated_habit is not None:
            habit = Habit.objects.get(pk=associated_habit.pk)

            if not habit.is_pleasurable:
                raise ValidationError('Связанная привычка должна быть приятной')
