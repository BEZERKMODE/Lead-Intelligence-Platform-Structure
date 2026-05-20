import logging

logger = logging.getLogger(__name__)

class AuditLogger:

    def log_action(
        self,
        user_id,
        action
    ):

        logger.info(
            f"USER={user_id} ACTION={action}"
        )

        return {
            "status": "logged"
        }
