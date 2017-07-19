from datetime import timedelta

BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost'

CELERYBEAT_SCHEDULE = {
    'validate': {
        'task': 'celery_app.tasks.validate',
        'schedule': timedelta(minutes=20),
    },
    'refresh': {
        'task': 'celery_app.tasks.refresh',
        'schedule': timedelta(minutes=60),
    },
}
