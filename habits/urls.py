from django.urls import path

from rest_framework.routers import SimpleRouter
from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView,
    HabitRetrieveAPIView,
    HabitListAPIView,
    HabitPublicListAPIView,
)

app_name = HabitsConfig.name
router = SimpleRouter()

urlpatterns = [
    path("create/", HabitCreateAPIView.as_view(),
         name="habit_create"),
    path("<int:pk>/update/", HabitUpdateAPIView.as_view(),
         name="habit_update"),
    path("<int:pk>/delete/", HabitDestroyAPIView.as_view(),
         name="habit_delete"),
    path("<int:pk>/", HabitRetrieveAPIView.as_view(),
         name="habit_get"),
    path("list/", HabitListAPIView.as_view(), name="habits_list"),
    path("public_list/", HabitPublicListAPIView.as_view(),
         name="habits-public_list"),
]

urlpatterns += router.urls
