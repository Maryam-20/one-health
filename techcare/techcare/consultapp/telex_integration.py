import httpx
import logging
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

TELEX_WEBHOOK_URL = "https://ping.telex.im/v1/webhooks/019522d7-22de-73d1-b411-ed0a5d6e024f"

async def send_appointment_notification(appointment):
    """Send notification to Telex when an appointment is created and doctor assigned"""
    
    data = {
        "username": "Hospital Appointment Bot",
        "event_name": "New Appointment",
        "status": "success",
        "message": f"New appointment created!\n"
                  f"Patient: {appointment.user.get_full_name() or appointment.user.username}\n"
                  f"Service: {appointment.service_option}\n"
                  f"Doctor Assigned: {appointment.assigned_doctor}\n"
                  f"Date Requested: {appointment.requested_date}"
    }
    
    logger.info(f"Attempting to send notification to Telex: {data}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(TELEX_WEBHOOK_URL, json=data)
            response.raise_for_status()
            logger.info(f"Successfully sent notification to Telex. Response: {response.status_code}")
            return True
    except Exception as e:
        logger.error(f"Failed to send Telex notification: {str(e)}")
        return False

async def test_telex_connection():
    """Test function to verify Telex webhook connection"""
    test_data = {
        "username": "Hospital Test Bot",
        "event_name": "Test Connection",
        "status": "test",
        "message": "This is a test message from the Hospital System"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(TELEX_WEBHOOK_URL, json=test_data)
            response.raise_for_status()
            return True, "Test message sent successfully"
    except Exception as e:
        return False, f"Connection test failed: {str(e)}" 