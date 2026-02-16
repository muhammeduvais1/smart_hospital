import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hospital.settings')
django.setup()

from django.contrib.auth import get_user_model

def make_superuser(username='admin', email='admin@example.com', password='AdminPass123!'):
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        print(f'Superuser "{username}" already exists.')
        return
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Created superuser: {username} / {password}')

if __name__ == '__main__':
    make_superuser()
