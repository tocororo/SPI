from celery import Celery

CELERY_BROKER_URI = "redis://10.16.64.51:6379/0"
CELERY_BACKEND_URI = "redis://10.16.64.51:6379/0"


def create_celery_app():
    celery_app = Celery(
        __name__,
        broker=CELERY_BROKER_URI,
        backend=CELERY_BACKEND_URI
        )
    return celery_app
