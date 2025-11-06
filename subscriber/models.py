from django.db import models
from cryptography.fernet import Fernet
import os
import logging

logger = logging.getLogger(__name__)


def get_encryption_key():
    """Get or generate encryption key for password encryption"""
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        # Generate a key if not set (not ideal for production, but works for dev)
        key = Fernet.generate_key()
        logger.warning("ENCRYPTION_KEY not set in environment. Using generated key (not persistent!)")
    else:
        # Environment variable is always a string, convert to bytes
        if isinstance(key, str):
            key = key.encode()
    return key


class Subscriber(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    encrypted_password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'

    def set_password(self, plain_password):
        """Encrypt and store password"""
        try:
            key = get_encryption_key()
            f = Fernet(key)
            encrypted = f.encrypt(plain_password.encode())
            self.encrypted_password = encrypted.decode()
        except Exception as e:
            logger.error(f"Error encrypting password: {e}")
            raise

    def get_password(self):
        """Decrypt and return password"""
        try:
            key = get_encryption_key()
            f = Fernet(key)
            decrypted = f.decrypt(self.encrypted_password.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Error decrypting password: {e}")
            return "***ERROR***"

    def __str__(self):
        return self.email
