from horilla_common.celery_app import task_retry_kwargs
from app.celery_worker import celery_app

@celery_app.task(**task_retry_kwargs())
def send_offer_letter(candidate_id: int):
    return {"status": "sent", "candidate_id": candidate_id}
