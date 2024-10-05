# Users/tests/test_models.py
import pytest
from django_countries.fields import Country
from django.core.exceptions import ValidationError
from django.utils import timezone
from Users.models import User, FreelancerProfile, Skill, Education, WorkExperience, Certification, Portfolio, ClientProfile
from Projects.models import Project, Milestone, Task, ProjectFreelancer, Application, Contract

@pytest.fixture
def client_user():
    return User.objects.create_user(
        username="client_user",
        password="password123",
        user_type="client"
    )

@pytest.fixture
def freelancer_user():
    return User.objects.create_user(
        username="freelancer_user",
        password="password123",
        user_type="freelancer"
    )

@pytest.fixture
def client_profile(client_user):
    return ClientProfile.objects.create(
        user=client_user,
        company_name="Tech Co.",
        company_website="http://techco.com",
        country="US",
        city="San Francisco",
        phone="123456789",
        address="1234 Tech St."
    )

@pytest.fixture
def freelancer_profile(freelancer_user):
    return FreelancerProfile.objects.create(
        user=freelancer_user,
        country="US",
        city="New York",
        phone="123456789",
        address="1234 Freelance Ave"
    )

@pytest.mark.django_db
def test_project_creation(client_profile):
    project = Project.objects.create(
        title="New Project",
        client=client_profile,
        start_date="2023-01-01",
        due_date="2023-12-31",
        description="Project description",
        budget=10000.00,
        category="web_development"
    )
    assert project.title == "New Project"
    assert project.client == client_profile
    assert project.start_date == timezone.datetime(2023, 1, 1).date()
    assert project.due_date == timezone.datetime(2023, 12, 31).date()
    assert project.description == "Project description"
    assert project.budget == 10000.00
    assert project.category == "web_development"

@pytest.mark.django_db
def test_milestone_creation(project):
    milestone = Milestone.objects.create(
        project=project,
        title="Milestone 1",
        description="Milestone description",
        due_date="2023-06-30",
        category="development"
    )
    assert milestone.project == project
    assert milestone.title == "Milestone 1"
    assert milestone.description == "Milestone description"
    assert milestone.due_date == timezone.datetime(2023, 6, 30).date()
    assert milestone.category == "development"

@pytest.mark.django_db
def test_task_creation(milestone, freelancer_profile):
    task = Task.objects.create(
        milestone=milestone,
        title="Task 1",
        description="Task description",
        due_date="2023-06-15",
        priority="high",
        status="pending",
        assigned_to=freelancer_profile
    )
    assert task.milestone == milestone
    assert task.title == "Task 1"
    assert task.description == "Task description"
    assert task.due_date == timezone.datetime(2023, 6, 15).date()
    assert task.priority == "high"
    assert task.status == "pending"
    assert task.assigned_to == freelancer_profile

@pytest.mark.django_db
def test_project_freelancer_creation(project, freelancer_profile):
    project_freelancer = ProjectFreelancer.objects.create(
        project=project,
        freelancer=freelancer_profile,
        status="accepted"
    )
    assert project_freelancer.project == project
    assert project_freelancer.freelancer == freelancer_profile
    assert project_freelancer.status == "accepted"

@pytest.mark.django_db
def test_application_creation(project, freelancer_profile):
    application = Application.objects.create(
        freelancer=freelancer_profile,
        project=project
    )
    assert application.freelancer == freelancer_profile
    assert application.project == project

@pytest.mark.django_db
def test_contract_creation(project, freelancer_profile):
    contract = Contract.objects.create(
        project=project,
        freelancer=freelancer_profile,
        start_date="2023-01-01",
        status="active"
    )
    assert contract.project == project
    assert contract.freelancer == freelancer_profile
    assert contract.start_date == timezone.datetime(2023, 1, 1).date()
    assert contract.status == "active"

@pytest.mark.django_db
def test_project_days_until_due(project):
    project.start_date = timezone.datetime(2023, 1, 1).date()
    project.due_date = timezone.datetime(2023, 12, 31).date()
    project.save()
    assert project.days_until_due() == "364 days to 2023-12-31"

@pytest.mark.django_db
def test_project_str_method(project):
    assert str(project) == f"{project.title} by {project.client.user.username}"

@pytest.mark.django_db
def test_milestone_str_method(milestone):
    assert str(milestone) == f"{milestone.title} - {milestone.project.title}"

@pytest.mark.django_db
def test_task_str_method(task):
    assert str(task) == task.title

@pytest.mark.django_db
def test_project_freelancer_str_method(project_freelancer):
    assert str(project_freelancer) == f"{project_freelancer.project.title} - {project_freelancer.freelancer.user.username} ({project_freelancer.status})"

@pytest.mark.django_db
def test_application_str_method(application):
    assert str(application) == f"{application.freelancer.user.username} applied to {application.project.title}"

@pytest.mark.django_db
def test_contract_str_method(contract):
    assert str(contract) == f"Contract for {contract.freelancer.user.username} on project {contract.project.title}"
