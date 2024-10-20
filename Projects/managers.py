# Projects/managers.py

from django.db import models

class ActiveManager(models.Manager):
    """Administrador que filtra objetos no eliminados."""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
