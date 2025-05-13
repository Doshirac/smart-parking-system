import json
import logging

logger = logging.getLogger(__name__)

def publish_event(event_type: str, payload: dict):
    event = {
        "type": event_type,
        "payload": payload
    }
    logger.info(f"Publishing event: {json.dumps(event)}")

def handle_payment_status_change(payment_data: dict):
    publish_event(f"Payment{payment_data['status'].capitalize()}", payment_data)
