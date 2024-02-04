from time import sleep
from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import EdlEntry


@shared_task()
def test_task_sample(a, b):
    ans = a + b
    return {
        'status': True,
        'ans': ans,
    }


@shared_task
def remove_expired_edl_entries():

    two_days_ago = now() - timedelta(days=2)

    # Filter entries that have been expired for at least 1 days
    expired_entries = EdlEntry.objects.filter(valid_until__lt=two_days_ago)


    # Count the entries for logging or debugging purposes
    count = expired_entries.count()

    try:
        # Delete the expired entries
        expired_entries.delete()
    # Delete the expired entries
    except Exception as e:
        return {
            'status': False,
            'message': f"An error occurred: {e}"
        }

    return {
        'status': True,
        'message': f"{count} entries have been deleted"
    }