#!/bin/bash
set -euo pipefail

# Only run migrations if not already applied
if [ ! -f /app/migrations.lock ]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput
    touch /app/migrations.lock
fi

# Collect static files once
if [ ! -f /app/staticfiles.lock ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear
    touch /app/staticfiles.lock
fi


# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations --noinput dataexposure
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create demo users if enabled
if [ "${CREATE_DEMO_USERS:-1}" = "1" ]; then
    echo "Setting up demo users..."
    python manage.py shell <<EOF
from django.contrib.auth.models import User
from dataexposure.models import UserData
import os

# Main demo user
demo_user, created = User.objects.get_or_create(
    username='demo',
    defaults={
        'email': 'demo@example.com',
        'password': os.environ.get('DEMO_PASSWORD', 'demo_password_123!')
    }
)

if created:
    UserData.objects.create(
        user=demo_user,
        credit_card='4111111111111111',
        ssn='123-45-6789',
        api_key=f"demo_key_{os.urandom(16).hex()}"
    )
    print("Created demo user with test data")

# Additional test users
test_users = [
    {'username': 'user1', 'cc': '5555555555554444', 'ssn': '987-65-4321'},
    {'username': 'user2', 'cc': '371449635398431', 'ssn': '456-78-9123'},
    {'username': 'user3', 'cc': '6011111111111117', 'ssn': '789-12-3456'}
]

for user_data in test_users:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': f"{user_data['username']}@example.com",
            'password': f"{user_data['username']}_password_123!"
        }
    )
    
    if created:
        UserData.objects.create(
            user=user,
            credit_card=user_data['cc'],
            ssn=user_data['ssn'],
            api_key=f"{user_data['username']}_key_{os.urandom(8).hex()}"
        )
        print(f"Created {user_data['username']} with test data")
EOF
fi

# Create superuser if enabled
if [ "${CREATE_SUPERUSER:-0}" = "1" ]; then
    echo "Creating superuser..."
    python manage.py shell <<EOF
from django.contrib.auth.models import User
import os

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        'admin',
        'admin@example.com',
        os.environ.get('ADMIN_PASSWORD', 'admin_password_123!')
    )
    print("Admin user created")
else:
    print("Admin user already exists")
EOF
fi

echo "✅ Setup complete! Starting server..."
exec "$@"