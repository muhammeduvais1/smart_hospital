import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hospital.settings')
django.setup()

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

GROUPS = ['Admin', 'Doctor', 'Nurse', 'Patient']

def create_groups():
    for g in GROUPS:
        Group.objects.get_or_create(name=g)
    print('Groups ensured:', GROUPS)

def assign_admin(username='admin'):
    User = get_user_model()
    try:
        u = User.objects.get(username=username)
        admin_group = Group.objects.get(name='Admin')
        u.groups.add(admin_group)
        u.is_staff = True
        u.save()
        print(f'Assigned {username} to Admin group and marked staff')
    except User.DoesNotExist:
        print(f'User {username} not found')

if __name__ == '__main__':
    create_groups()
    assign_admin()
