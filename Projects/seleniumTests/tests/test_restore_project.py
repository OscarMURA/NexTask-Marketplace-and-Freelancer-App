import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.client_signup_page import ClientSignUpPage
from pages.project_creation_page import ProjectCreationPage
from pages.home_client_page import HomeClientPage
from pages.deleted_projects_page import DeletedProjectsPage




@pytest.mark.usefixtures("setup")
@pytest.mark.selenium
class TestRestoreProject:
    @pytest.mark.run(order=3)
    def test_restore_project(self):
        # Paso 1: Registro del cliente
        signup_page = ClientSignUpPage(self.driver)
        signup_page.go_to_signup_page()
        signup_page.fill_signup_form(
            username="testclient4321",
            email="client4321@example.com",
            first_name="Test3",
            last_name="Client3",
            company_name="TestCompany3",
            country="USA",
            city="Los Angeles",
            password="SecurePassword4321"
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
        delete_project_button = home_client_page.find_delete_button(3)  # Usamos el ID del proyecto (2 en este caso)
        delete_project_button.click()

        # Hacer clic en el botón "Remove" después de que el modal sea visible
        home_client_page.click_remove_button(3)

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

        # Paso 6: Hacer clic en el botón "Restore" para restaurar el proyecto
        deleted_projects_page.click_restore_button(3)

      
        # Paso 7: Verificar que el usuario ha sido redirigido a la página de home-client
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("home-Client")  # Asegura que la URL contiene 'home-Client'
        )
        assert "home-Client" in self.driver.current_url, "User was not redirected to home-client after restoring the project."

