from django_celery_beat.models import PeriodicTask, IntervalSchedule
from auth_app.tasks import test_periodic_task


# executes every 10 seconds.
schedule, created = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS,
)

PeriodicTask.objects.create(
    interval=schedule,                  # we created this above.
    name='Importing contacts',          # simply describes this periodic task.
    task=test_periodic_task  # name of task.
)