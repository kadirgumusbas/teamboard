import os
import django
import random
from faker import Faker

# Django ortamını başlat
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker()

def create_dummy_users(n=100):
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
        email = f"{username}@example.com"
        password = "testpassword123"

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
    print(f"{n} dummy users created successfully.")

if __name__ == "__main__":
    create_dummy_users()
