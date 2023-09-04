from django.urls import path
from .consumers import MySyncConsumer


ws_patterns = [
    path("sync/", MySyncConsumer.as_asgi()),
]
