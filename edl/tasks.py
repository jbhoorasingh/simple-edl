from time import sleep
from celery import shared_task


@shared_task()
def test_task_sample(a, b):
    ans = a + b
    return {
        'status': True,
        'ans': ans,
    }