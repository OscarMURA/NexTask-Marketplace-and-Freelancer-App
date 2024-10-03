# Comments/models.py

from django.db import models
from django.contrib.auth import get_user_model
from Projects.models import Task

User = get_user_model()

class Comment(models.Model):
    """
    Modelo que representa un comentario en una tarea.

    Atributos:
        task (Task): La tarea a la que está asociado el comentario.
        author (User): El usuario que creó el comentario.
        content (str): El contenido del comentario.
        created_at (datetime): La fecha y hora en que se creó el comentario.
    """
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.author.username} en {self.task.title}'
