import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.home_client_page import HomeClientPage
from pages.applications_page import ApplicationsPage
from pages.project_detail_page import ProjectDetailPage

@pytest.mark.usefixtures("setup")
class TestAcceptFreelancerApplication:
    @pytest.mark.run(order=5)
    def test_accept_freelancer_application(self):
        # Paso 1: Login como cliente
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()

        # Completar el formulario de login
        login_page.login(username="testclient123", password="SecurePassword123")

        # Redirigir a Home-Client
        self.driver.get("http://127.0.0.1:8000/en/projects/home-Client/")
        assert "home-Client" in self.driver.current_url, "Client not redirected to home-Client."

        # Paso 2: Hacer clic en el botón "View Project" del proyecto específico
        home_client_page = HomeClientPage(self.driver)
        home_client_page.click_view_project_button()

        # Paso 3: Hacer clic en "Manage Applications Freelancer"
        home_client_page.click_manage_applications_button()

        # Paso 4: Hacer clic en el botón "Accept" para aceptar la aplicación del freelancer
        applications_page = ApplicationsPage(self.driver)

        # Esperamos hasta que el botón "Accept" sea clickeable y lo hacemos clic
        accept_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "accetp_applFreelancer_btt"))
        )
        accept_button.click()

        # Paso 5: Verificar que la página redirige a home-Client después de aceptar la aplicación
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be("http://127.0.0.1:8000/en/projects/home-Client/")
        )
        assert "home-Client" in self.driver.current_url, "Not redirected to home-Client after accepting application."
