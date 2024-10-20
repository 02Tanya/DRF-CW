from users.models import User
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Пользователь",
        help_text="Укажите пользователя",
        null=True,
        blank=True,
    )
    place = models.CharField(
        max_length=150,
        verbose_name="Место",
        help_text="Укажите место",
        null=True,
        blank=True,
    )
    time = models.TimeField(
        verbose_name="Время", help_text="Укажите время", null=True, blank=True
    )
    periodicity = models.PositiveIntegerField(
        verbose_name="Периодичность, дн.",
        help_text="Укажите периодичность в днях",
        default=1,
    )
    action = models.CharField(
        max_length=150,
        verbose_name="Состав привычки",
        help_text="Укажите, в чем состоит привычка",
    )
    is_pleasurable = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Укажите, приятная ли привычка",
    )
    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Укажите связанную привычку",
        null=True,
        blank=True,
    )
    reward = models.CharField(
        verbose_name="Вознаграждение",
        help_text="Укажите вознаграждение",
        null=True,
        blank=True,
    )
    lead_time = models.IntegerField(
        verbose_name="Время на выполнение", help_text="Укажите время на выполнение"
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная привычка",
        help_text="Укажите, является ли привычка публичной",
    )
    date_of_next_reminder_sending = models.DateField(
        verbose_name="Дата отправки следующего напоминания",
        help_text="Укажите дату для отправки следующего напоминания",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-time"]

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"
