# Django Signup System with n8n and Retell Integration

A production-ready Django signup system that captures user email subscriptions, generates secure passwords, sends welcome emails, triggers n8n webhooks for Google Sheets integration, and initiates automated voice calls via Retell API.

## Features

- **User Subscription Form**: HTML form for email subscription (name optional)
- **Secure Password Generation**: 8-character random password generation
- **Encrypted Password Storage**: Passwords encrypted in database using Fernet symmetric encryption
- **Welcome Email**: Automated email with password and welcome message
- **n8n Webhook Integration**: Triggers n8n workflow for Google Sheets and Retell API integration
- **Django Admin Panel**: View all subscribers with decrypted passwords

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Copy `env.example` to `.env` and configure the following variables:

```bash
# Generate encryption key first
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Then set in .env file
ENCRYPTION_KEY=your-generated-key-here
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/your-webhook-id
RETELL_API_KEY=your-retell-api-key
```

**Important**: For Gmail, you'll need to use an App Password (not your regular password). Enable 2FA and generate an app password in your Google Account settings.

### 3. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

### 6. Access the Application

- **Subscription Form**: http://localhost:8000/subscribe/
- **Admin Panel**: http://localhost:8000/admin/

## Testing Email (Development)

For testing without SMTP, you can use console backend:

```bash
export EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
python manage.py runserver
```

Emails will be printed to the console instead of being sent.

## n8n Workflow Setup

Your n8n workflow should:

1. **Webhook Trigger**: Receive POST requests with:
   - `name` (string, optional)
   - `email` (string)
   - `password` (string, plain text)
   - `timestamp` (ISO format string)

2. **Google Sheets Node**: Append data to "UserSubscriptions" sheet with columns:
   - Name
   - Email
   - Password
   - Timestamp

3. **Retell API Node**: Initiate voice call using Retell API
   - Use the provided `RETELL_API_KEY`
   - Custom script thanking user for registering
   - Introduce Infugin Technologies as a leader in development, automation, and AI services

4. **Error Handling**: Log or email errors for sheet write failures and call failures

## Project Structure

```
siginup_backend/
├── subscriber/
│   ├── models.py          # Subscriber model with encrypted password
│   ├── views.py           # Subscribe view with password generation
│   ├── forms.py           # Subscription form
│   ├── admin.py           # Admin configuration
│   ├── utils.py           # Webhook utility functions
│   └── templates/
│       └── subscriber/
│           ├── subscribe.html      # Subscription form template
│           └── welcome_email.html  # Email template
├── siginup_backend/
│   ├── settings.py        # Django settings with email/webhook config
│   └── urls.py            # URL routing
├── requirements.txt       # Python dependencies
└── env.example            # Environment variable template
```

## Security Notes

- Passwords are encrypted in the database using Fernet symmetric encryption
- Plain text passwords are only sent in emails and webhooks (encrypted for storage)
- Keep `ENCRYPTION_KEY` secure and never commit it to version control
- Use environment variables for all sensitive settings
- In production, use proper SMTP credentials and secure HTTPS

## Testing

1. **Form Submission**: Visit `/subscribe/` and submit the form
2. **Email Verification**: Check email inbox (or console if using console backend)
3. **Admin Panel**: View subscribers at `/admin/` with decrypted passwords
4. **Webhook**: Check n8n workflow logs for webhook triggers
5. **Database**: Verify subscriber is saved in database

## Troubleshooting

- **Email not sending**: Check SMTP credentials and ensure EMAIL_BACKEND is set correctly
- **Encryption errors**: Ensure ENCRYPTION_KEY is set and consistent
- **Webhook not triggering**: Verify N8N_WEBHOOK_URL is correct and accessible
- **Admin password not showing**: Check encryption key is correct and logging for errors

## Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in settings.py
2. Generate a new `SECRET_KEY`
3. Set proper `ALLOWED_HOSTS`
4. Use secure SMTP credentials
5. Set up proper logging
6. Use environment variables for all sensitive data
7. Ensure HTTPS is enabled
8. Keep encryption key secure and backed up

