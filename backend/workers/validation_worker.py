from backend.celery_worker import celery

from backend.services.email_validator import EmailValidator

validator = EmailValidator()

@celery.task
def validate_email(email):

    return validator.validate_email(email)
