import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from pages.client_signup_page import ClientSignUpPage
from pages.project_creation_page import ProjectCreationPage
from pages.home_client_page import HomeClientPage
from pages.deleted_projects_page import DeletedProjectsPage


@pytest.mark.usefixtures("setup")
class TestDeleteProject:
    @pytest.mark.run(order=2)
    def test_delete_project(self):
        # Paso 1: Registro del cliente
        signup_page = ClientSignUpPage(self.driver)
        signup_page.go_to_signup_page()
        signup_page.fill_signup_form(
            username="testclient321",
            email="client321@example.com",
            first_name="Test2",
            last_name="Client2",
            company_name="TestCompany2",
            country="USA",
            city="Los Angeles",
            password="SecurePassword321"
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
            category="web_development",
            description="Descripción detallada del proyecto"
        )
        project_page.submit_form()

        # Confirmación de redirección al home-client después de crear el proyecto
        assert "home-Client" in self.driver.current_url, "Failed to redirect to home-client after project creation"

        # Paso 3: Eliminar el proyecto
        home_client_page = HomeClientPage(self.driver)

        # Localizar y hacer clic en el botón de eliminación del proyecto usando el ID dinámico
        delete_project_button = home_client_page.find_delete_button(2)  # Usamos el ID del proyecto (2 en este caso)
        delete_project_button.click()

        # Hacer clic en el botón "Remove" después de que el modal sea visible
        home_client_page.click_remove_button(2)

        # Confirmación de que el proyecto ya no aparece en el home-client
        assert "Proyecto de Prueba" not in self.driver.page_source, "Project was not deleted from home-client"

        # Paso 4: Verificar que el mensaje "No projects available" está presente en la página después de eliminar el proyecto
        no_projects_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'No projects available.')]"))
        )

        assert no_projects_message.text == "No projects available.", "The 'No projects available.' message was not displayed."

        # Paso 5: Verificar que el proyecto eliminado aparece en la página de proyectos eliminados
        self.driver.get("http://127.0.0.1:8000/en/projects/projects/deleted/")

        deleted_projects_page = DeletedProjectsPage(self.driver)

        # Verificar que el proyecto eliminado está en la lista de proyectos eliminados  
        assert "Proyecto de Prueba" in deleted_projects_page.get_deleted_project_titles(), "Deleted project not found in the deleted projects page"   

        # Paso 6: Hacer clic en el botón "Delete Permanently" y confirmar la alerta
        deleted_projects_page.click_delete_permanently_button(2)

        # Verificar que el proyecto ya no está en la lista de proyectos eliminados después de la eliminación permanente
        WebDriverWait(self.driver, 10).until(
            EC.staleness_of(delete_project_button)
        )

        # Confirmar que el proyecto ya no está en la página de proyectos eliminados
        assert "Proyecto de Prueba" not in deleted_projects_page.get_deleted_project_titles(), "Project was not permanently deleted."
