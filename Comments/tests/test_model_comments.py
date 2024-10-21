import json
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from Comments.models import Comment
from Projects.models import Task, Milestone, Project
from Users.models import ClientProfile

User = get_user_model()

@pytest.mark.django_db
def test_create_comment():
    # Crea un usuario para usar en la prueba
    user = User.objects.create_user(username='testuser', password='password123')

    # Crea un cliente para el proyecto
    client = ClientProfile.objects.create(user=user)  # Asumiendo que 'user' es un campo de 'ClientProfile'

    # Crea un proyecto para asociar el hito
    project = Project.objects.create(
        title='Test Project',
        client=client,  # Proporciona el cliente
        description=json.dumps({
            "delta": {
                "ops": [{"insert": "A test project.\n"}]
            }
        }),
        start_date=timezone.now(),  # Asigna una fecha de inicio válida
        due_date='2024-12-31',  # Asegúrate de proporcionar la fecha de vencimiento
        budget=1000.00,  # Asigna un presupuesto válido
        category='development'  # Proporciona una categoría válida
    )

    # Crea un hito con contenido válido para QuillField
    milestone = Milestone.objects.create(
        project=project,
        title='Test Milestone',
        description=json.dumps({
            "delta": {
                "ops": [{"insert": "A milestone for testing.\n"}]
            }
        }),
        start_date=timezone.now(),  # Asigna una fecha de inicio válida
        due_date='2024-12-31',
        category='development'
    )

    # Crea una tarea asociada al hito
    task = Task.objects.create(
        milestone=milestone,
        title='Test Task',
        description=json.dumps({
            "delta": {
                "ops": [{"insert": "A test task.\n"}]
            }
        }),  # Asegúrate de que esto sea un JSON válido para QuillField
        start_date=timezone.now(),  # Asigna una fecha de inicio válida
        due_date='2024-12-31',  # Asigna una fecha válida
        priority='medium',  # Asigna una prioridad válida
        status='pending'  # Asigna un estado válido
    )

    # Crea un comentario asociado a la tarea y al usuario
    comment = Comment.objects.create(task=task, author=user, content='This is a test comment.')

    # Verifica que el comentario se haya creado correctamente
    assert comment.task == task
    assert comment.author == user
    assert comment.content == 'This is a test comment.'
    assert comment.created_at <= timezone.now()  # Asegúrate de que la fecha se haya establecido
    assert str(comment) == 'Comentario de testuser en Test Task'