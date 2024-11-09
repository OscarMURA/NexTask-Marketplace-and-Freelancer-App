# Comments/models.py

from django.db import models
from django.contrib.auth import get_user_model
from Projects.models import Task
from Users.models import FreelancerProfile


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
    
    
class FreelancerComment(models.Model):
    """
    Modelo que representa un comentario y calificación en el perfil de un freelancer.
    
    Atributos:
        freelancer (FreelancerProfile): El perfil del freelancer al que se asocia el comentario.
        user (User): El usuario que realiza el comentario.
        rating (int): Calificación del freelancer (1 a 5 estrellas).
        comment (str): Contenido del comentario.
        created_at (datetime): Fecha y hora de creación del comentario.
    """
    freelancer = models.ForeignKey(FreelancerProfile, related_name='freelancer_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('freelancer', 'user')  # Cada usuario puede comentar una vez por freelancer
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Comentario de {self.user.username} en {self.freelancer.user.username}'
