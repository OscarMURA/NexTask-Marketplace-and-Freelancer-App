from django.test import TestCase
from django.urls import reverse
from Projects.models import Project, ProjectFreelancer, Task
from Users.models import FreelancerProfile, ClientProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class ReportViewsTest(TestCase):

    def setUp(self):
        """
        Configuración inicial de usuarios, perfiles, proyectos, tareas y asociaciones.
        """
        # Crear usuarios
        self.freelancer_user = User.objects.create_user(username='freelancer', password='password')
        self.client_user = User.objects.create_user(username='client', password='password')

        # Crear perfiles asociados
        self.freelancer_profile = FreelancerProfile.objects.create(user=self.freelancer_user)
        self.client_profile = ClientProfile.objects.create(user=self.client_user)

        # Crear proyectos y asociarlos al cliente
        self.project1 = Project.objects.create(
            title='Project 1',
            client=self.client_profile,
            start_date='2024-01-01',
            due_date='2024-02-01',
            actual_end_date=None,
            description='{"delta": {}, "html": "<p>Project description 1</p>"}',
            budget=1000.00,
            category='web_development'
        )

        self.project2 = Project.objects.create(
            title='Project 2',
            client=self.client_profile,
            start_date='2024-03-01',
            due_date='2024-04-01',
            actual_end_date='2024-04-02',
            description='{"delta": {}, "html": "<p>Project description 2</p>"}',
            budget=2000.00,
            category='graphic_design'
        )

        # Asociar freelancer a proyectos
        ProjectFreelancer.objects.create(project=self.project1, freelancer=self.freelancer_profile, status='accepted')
        ProjectFreelancer.objects.create(project=self.project2, freelancer=self.freelancer_profile, status='accepted')

        # Crear tareas asociadas
        Task.objects.create(
            milestone=self.project1.milestones.create(
                title="Milestone 1",
                start_date="2024-01-01",
                due_date="2024-01-10",
                description='{"delta": {}, "html": "<p>Milestone 1 description</p>"}',
            ),
            title="Task 1",
            start_date="2024-01-02",
            due_date="2024-01-08",
            description='{"delta": {}, "html": "<p>Task 1 description</p>"}',
            priority="high",
            status="completed",
            assigned_to=self.freelancer_profile
        )

        Task.objects.create(
            milestone=self.project2.milestones.create(
                title="Milestone 2",
                start_date="2024-03-01",
                due_date="2024-03-10",
                description='{"delta": {}, "html": "<p>Milestone 2 description</p>"}',
            ),
            title="Task 2",
            start_date="2024-03-02",
            due_date="2024-03-08",
            description='{"delta": {}, "html": "<p>Task 2 description</p>"}',
            priority="medium",
            status="in_progress",
            assigned_to=self.freelancer_profile
        )

    