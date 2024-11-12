import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.home_client_page import HomeClientPage
from pages.project_detail_client import ProjectDetailClientPage
from pages.freelancers_in_project_page import FreelancersInProjectPage
@pytest.mark.usefixtures("setup")
class TestClientFreelancerNavigation:
    @pytest.mark.run(order=11)
    def test_client_freelancer_navigation(self):
        # Paso 1: Login como client
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        login_page.login(username="testclient123", password="SecurePassword123")

        # Paso 2: Ir al Home-Client
        self.driver.get("http://127.0.0.1:8000/en/projects/home-Client/")
        
        # Wait for page to load fully, checking that we are at the correct URL
        WebDriverWait(self.driver, 20).until(
            EC.url_to_be("http://127.0.0.1:8000/en/projects/home-Client/")
        )
        
        # Ensure the exact URL matches
        assert self.driver.current_url == "http://127.0.0.1:8000/en/projects/home-Client/", f"Client not redirected to home-Client. Current URL: {self.driver.current_url}"

        # Paso 3: Hacer clic en el botón 'Ver Proyecto'
        home_client_page = HomeClientPage(self.driver)
        home_client_page.click_view_project_button()

        # Paso 4: Asegurarse que estamos en la página de detalles del proyecto
        project_detail_page = ProjectDetailClientPage(self.driver)
        WebDriverWait(self.driver, 20).until(
            EC.url_to_be("http://127.0.0.1:8000/en/projects/project/1/")
        )
        assert "project/1/" in self.driver.current_url, "Not redirected to project details page."

        # Paso 5: Hacer clic en 'Freelancer List in the project'
        project_detail_page.click_freelancers_in_project_button()

        # Paso 6: Asegurarse que estamos en la página de freelancers en el proyecto
        freelancers_in_project_page = FreelancersInProjectPage(self.driver)
        WebDriverWait(self.driver, 20).until(
            EC.url_to_be("http://127.0.0.1:8000/en/projects/projects/1/freelancers/")
        )
        assert "freelancers" in self.driver.current_url, "Not redirected to freelancers in project page."

        # Paso 7: Verificar que 'testfreelancer123' está en la lista de freelancers
        freelancer_name = freelancers_in_project_page.get_freelancer_name()
        assert freelancer_name == "testfreelancer123", f"Expected freelancer 'testfreelancer123', but found {freelancer_name}."