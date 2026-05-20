from backend.celery_worker import celery

@celery.task
def monitor_system():

    return {
        "status": "healthy",
        "workers_running": True
    }
