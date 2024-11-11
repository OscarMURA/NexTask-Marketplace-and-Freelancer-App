import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.freelancer_signup_page import FreelancerSignUpPage
from pages.home_freelancer_page import HomeFreelancerPage
from pages.search_projects_page import SearchProjectsPage
from pages.project_detail_page import ProjectDetailPage
from pages.login_page import LoginPage
from pages.home_client_page import HomeClientPage
from pages.applications_page import ApplicationsPage

@pytest.mark.usefixtures("setup")
class TestDeniedFreelancerApplication:
    @pytest.mark.run(order=1)
    def test_denied_freelancer_application(self):
        # Paso 1: Registro del freelancer
        signup_page = FreelancerSignUpPage(self.driver)
        signup_page.go_to_signup_page()

        # Completar el formulario de registro del freelancer con nuevos campos
        signup_page.fill_signup_form(
            username="testfreelancer321",
            first_name="Jane",
            last_name="Smith",
            phone="9876543210",
            email="freelancer321@example.com",
            country="USA",
            city="Los Angeles",
            address="456 Maple St",
            password="SecurePassword321",
            confirm_password="SecurePassword321"
        )

        # Enviar el formulario
        signup_page.submit_form()

        # Paso 2: Redirigir manualmente al Home-Freelancer (si es que no ocurre automáticamente)
        self.driver.get("http://127.0.0.1:8000/en/users/Home-Freelancer/")

        # Paso 3: Confirmar que se ha redirigido correctamente al dashboard del freelancer
        assert "Home-Freelancer" in self.driver.current_url, "Freelancer not redirected to home-Freelancer."

        # Paso 4: Hacer clic en el botón de "Search Projects"
        home_freelancer_page = HomeFreelancerPage(self.driver)

        # Esperar hasta que el botón 'Search Projects' esté disponible y hacer clic
        search_projects_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_search_project"))
        )
        search_projects_button.click()

        # Confirmar que se ha redirigido a la página de búsqueda de proyectos
        assert "search_projects" in self.driver.current_url, "Freelancer not redirected to search projects page."

        # Paso 5: Hacer clic en un proyecto específico (en este caso, el proyecto con ID=1)
        search_projects_page = SearchProjectsPage(self.driver)
        search_projects_page.click_on_project(1)  # Usamos el ID del proyecto (ajustarlo según el caso)

        # Confirmar que estamos en la página de detalles del proyecto
        project_detail_page = ProjectDetailPage(self.driver)
        assert "project/view" in self.driver.current_url, "Not redirected to project details page."

        # Paso 6: Hacer clic en el botón "Apply to Project"
        project_detail_page.click_apply_button()

        # Paso 7: Verificar que el mensaje "Application Submitted!" se muestra
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Application Submitted!')]"))
        )
        application_message = self.driver.find_element(By.XPATH, "//h4[contains(text(), 'Application Submitted!')]")
        assert application_message.text == "Application Submitted!", "Application submission failed."

        # Paso 8: Login como cliente y gestionar las aplicaciones
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()

        # Completar el formulario de login con el cliente
        login_page.login(username="testclient123", password="SecurePassword123")

        # Redirigir a Home-Client
        self.driver.get("http://127.0.0.1:8000/en/projects/home-Client/")
        assert "home-Client" in self.driver.current_url, "Client not redirected to home-Client."

        # Paso 9: Hacer clic en el botón "View Project" del proyecto específico
        home_client_page = HomeClientPage(self.driver)
        home_client_page.click_view_project_button()

        # Paso 10: Hacer clic en "Manage Applications Freelancer"
        home_client_page.click_manage_applications_button()

        # Paso 11: Hacer clic en el botón "Reject" para rechazar la aplicación del freelancer
        applications_page = ApplicationsPage(self.driver)

        # Esperamos hasta que el botón "Reject" sea clickeable y lo hacemos clic
        reject_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "denied_applFreelancer_btt"))
        )
        reject_button.click()

        # Paso 12: Verificar que la página redirige a home-Client después de rechazar la aplicación
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be("http://127.0.0.1:8000/en/projects/home-Client/")
        )
        assert "home-Client" in self.driver.current_url, "Not redirected to home-Client after rejecting application."
