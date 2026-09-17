"""
ASGI config for daniela_zabala_proyecto_final_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daniela_zabala_proyecto_final_core.settings')

application = get_asgi_application()
