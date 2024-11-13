# celery_worker.py
from celery import Celery
import os

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//"),  # RabbitMQ as broker
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")  # Redis as result backend
    # "tasks",
    # broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    # backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)

celery_app.conf.update(
    broker_transport_options={
        'max_retries': 5,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
    },
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_disable_rate_limits=True,
    worker_max_tasks_per_child=100,  # Prevent memory leaks by restarting workers after 100 tasks
    worker_prefetch_multiplier=1,    # Control task prefetching for load balancing
    worker_concurrency=4,  # Adjust concurrency based on your environment
    task_acks_late=True              # Acknowledge tasks after processing
)

# celery_app.autodiscover_tasks(["tasks.users_tasks"])  # Auto-discover tasks


import domains.aiti.apis.aiti_tasks
import domains.users.apis.users_tasks
# import routers.query_router.tasks