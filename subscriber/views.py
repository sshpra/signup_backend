import secrets
import string
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import SubscriptionForm
from .models import Subscriber
from .utils import send_n8n_webhook

logger = logging.getLogger(__name__)


def generate_password(length=8):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits
    # Exclude confusing characters like 0, O, I, l
    alphabet = alphabet.replace('0', '').replace('O', '').replace('I', '').replace('l', '')
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def subscribe_view(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data.get('name', '')

            # Check if email already exists
            if Subscriber.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered.')
                return render(request, 'subscriber/subscribe.html', {'form': form})

            # Generate password
            password = generate_password()

            try:
                # Create and save subscriber with encrypted password
                subscriber = Subscriber(email=email, name=name or None)
                subscriber.set_password(password)
                subscriber.save()

                # Send welcome email
                try:
                    email_subject = 'Welcome to Infugin Technologies!'
                    email_message = render_to_string('subscriber/welcome_email.html', {
                        'name': name or 'Valued Customer',
                        'email': email,
                        'password': password,
                    })
                    
                    send_mail(
                        email_subject,
                        email_message,
                        getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@infugin.com'),
                        [email],
                        html_message=email_message,
                        fail_silently=False,
                    )
                    logger.info(f"Welcome email sent to {email}")
                except Exception as e:
                    logger.error(f"Error sending welcome email to {email}: {e}", exc_info=True)
                    # Don't fail the subscription if email fails
                    messages.warning(request, 'Registration successful, but we encountered an issue sending your welcome email. Please contact support.')

                # Trigger n8n webhook (non-blocking)
                send_n8n_webhook(name, email, password)

                messages.success(request, 'Thank you for subscribing! Check your email for your password.')
                return redirect('subscribe')
            except Exception as e:
                logger.error(f"Error saving subscriber {email}: {e}", exc_info=True)
                messages.error(request, 'An error occurred during registration. Please try again.')
    else:
        form = SubscriptionForm()

    return render(request, 'subscriber/subscribe.html', {'form': form})
