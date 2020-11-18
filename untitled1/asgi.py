"""
ASGI config for untitled1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from channels.routing import get_default_application
from channels.layers import get_channel_layer
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'untitled1.settings')
# os.environ['ASGI_THREADS']="4"
django.setup()
application = get_default_application()
channel_layer = get_channel_layer()
