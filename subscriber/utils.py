import requests
import threading
import logging
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)


def send_n8n_webhook(name, email, password):
    """
    Send subscriber data to n8n webhook asynchronously
    """
    def _send_webhook():
        webhook_url = getattr(settings, 'N8N_WEBHOOK_URL', None)
        
        if not webhook_url:
            logger.warning("N8N_WEBHOOK_URL not configured. Skipping webhook call.")
            return

        payload = {
            'name': name or '',
            'email': email,
            'password': password,
            'timestamp': datetime.now().isoformat(),
        }

        try:
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"Successfully sent webhook for {email}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending webhook for {email}: {e}", exc_info=True)

    # Run webhook in background thread to avoid blocking
    thread = threading.Thread(target=_send_webhook)
    thread.daemon = True
    thread.start()

