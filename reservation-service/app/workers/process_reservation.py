import json
import logging

logger = logging.getLogger(__name__)

# Эмуляция публикации события в шину (например, Kafka, Redis, SNS/SQS и т.п.)
def publish_event(event_type: str, payload: dict):
    # Здесь должна быть интеграция с реальной шиной событий
    event = {
        "type": event_type,
        "payload": payload
    }
    logger.info(f"Publishing event: {json.dumps(event)}")
    # Например: kafka_producer.send("reservations", value=event)

# Обработчик события "ReservationCreated"
def handle_reservation_created(reservation_data: dict):
    logger.info(f"Handling reservation created: {reservation_data}")
    publish_event("ReservationCreated", reservation_data)

# Обработчик события "ReservationCompleted"
def handle_reservation_completed(reservation_data: dict):
    logger.info(f"Handling reservation completed: {reservation_data}")
    publish_event("ReservationCompleted", reservation_data)

# Пример: вызов после создания брони
if __name__ == "__main__":
    test_payload = {
        "reservation_id": 123,
        "user_id": 1,
        "spot_id": 5,
        "start_time": "2025-05-12T10:00:00Z",
        "end_time": "2025-05-12T12:00:00Z",
        "status": "reserved"
    }
    handle_reservation_created(test_payload)