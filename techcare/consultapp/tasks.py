from celery import shared_task
from .models import Appointment
from .telex_integration import send_appointment_notification
import asyncio
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_appointment_notification_task(appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Run the async notification in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            notification_sent = loop.run_until_complete(
                send_appointment_notification(appointment)
            )
            if notification_sent:
                logger.info(f"Notification sent for appointment {appointment_id}")
            else:
                logger.warning(f"Failed to send notification for appointment {appointment_id}")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error in notification task: {str(e)}")
        raise 