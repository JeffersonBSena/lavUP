import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lavup.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

client = Client(HTTP_HOST='127.0.0.1')
user, _ = User.objects.get_or_create(username='test_user', defaults={'email':'test@example.com'})
client.force_login(user)

urls = [
    'dashboard',
    'agenda',
    'clientes',
    'veiculos',
    'servicos',
    'usuarios',
    'configuracoes',
]

print("Testing Pages:")
for url_name in urls:
    url = reverse(url_name)
    try:
        response = client.get(url)
        print(f"[{response.status_code}] {url_name}")
        if response.status_code != 200:
            print(f"  Error snippet: {response.content.decode('utf-8')[:200]}")
    except Exception as e:
        print(f"[ERROR] {url_name}: {e}")

