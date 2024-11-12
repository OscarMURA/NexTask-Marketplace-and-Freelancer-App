from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from pages.client_signup_page import ClientSignUpPage
from pages.project_creation_page import ProjectCreationPage
from pages.milestone_creation_page import MilestoneCreationPage
from pages.task_creation_page import TaskCreationPage

@pytest.mark.usefixtures("setup")
class TestProjectMilestoneTask:
    @pytest.mark.run(order=1)
    def test_create_project_milestone_and_task(self):
        # Paso 1: Registro del cliente
        signup_page = ClientSignUpPage(self.driver)
        signup_page.go_to_signup_page()
        signup_page.fill_signup_form(
            username="testclient123",
            email="client123@example.com",
            first_name="Test",
            last_name="Client",
            company_name="TestCompany",
            country="USA",
            city="Los Angeles",
            password="SecurePassword123"
        )
        signup_page.submit_form()

        # Confirmación de la redirección al dashboard del cliente (home-client)
        assert "home-Client" in self.driver.current_url, "User registration failed or not redirected to client dashboard."

        # Paso 2: Crear el proyecto
        create_project_btn = self.driver.find_element(By.ID, "create-project-btn")
        create_project_btn.click()

        project_page = ProjectCreationPage(self.driver)
        project_page.fill_project_form(
            title="Proyecto de Prueba",
            start_date="01/12/2024",
            due_date="01/12/2025",
            budget="1000",
            category="Content-Writing",
            description="Descripción detallada del proyecto"
        )
        project_page.submit_form()

        # Confirmación de redirección al home-client después de crear el proyecto
        assert "home-Client" in self.driver.current_url, "Failed to redirect to home-client after project creation"

        # Paso 3: Redirección a la página de detalle del proyecto (usando ID 1)
        project_detail_url = "http://127.0.0.1:8000/en/projects/project/1/"
        self.driver.get(project_detail_url)
        
        

        
        milestone_url = "http://127.0.0.1:8000/en/projects/projects/1/add_milestone/"
        self.driver.get(milestone_url)

        milestone_page = MilestoneCreationPage(self.driver, 1)
        milestone_page.fill_milestone_form(
            title="Hito de Prueba",
            start_date="02/01/2024",
            due_date="03/01/2024",
            category="Development",
            description="Descripción del hito de prueba"
        )
        milestone_page.submit_form()

        # Confirmación de redirección al detalle del proyecto después de crear el milestone
        assert "/project/1/" in self.driver.current_url, "Failed to redirect to project detail after creating milestone"

        # Paso 5: Redirección a la página de detalle del milestone (usando ID 1)
        milestone_detail_url = "http://127.0.0.1:8000/en/projects/milestone/1/"
        
        
        self.driver.get(milestone_detail_url)

        # Paso 6: Redirección a la página de creación de task dentro del milestone
        task_url = "http://127.0.0.1:8000/en/projects/milestone/1/add_task/"
        self.driver.get(task_url)

        task_page = TaskCreationPage(self.driver, 1)
        task_page.fill_task_form(
            title="Tarea de Prueba",
            start_date="03/01/2024",
            due_date="04/01/2024",
            priority="High",
            status="In Progress",
            description="Descripción de la tarea de prueba"
        )
        task_page.submit_form()

        # Confirmación de redirección al detalle del milestone después de crear la tarea
        assert "/milestone/1/" in self.driver.current_url, "Failed to redirect to milestone detail after creating task"
