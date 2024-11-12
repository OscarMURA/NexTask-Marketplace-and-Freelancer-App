import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.home_freelancer_page import HomeFreelancerPage
from pages.search_projects_page import SearchProjectsPage

@pytest.mark.usefixtures("setup")
class TestSearchProject:
    @pytest.mark.run(order=8)
    def test_search_project_from_home_freelancer(self):    
        # Paso 1: Login como freelancer
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()

        # Completar el formulario de login con las credenciales del freelancer
        login_page.login(username="testfreelancer123", password="SecurePassword123")

        # Redirigir a Home-Freelancer
        self.driver.get("http://127.0.0.1:8000/en/users/Home-Freelancer/")
        assert "Home-Freelancer" in self.driver.current_url, "Freelancer not redirected to home-Freelancer."

        # Paso 2: Hacer clic en el botón 'Search Projects'
        home_freelancer_page = HomeFreelancerPage(self.driver)

        # Esperar hasta que el botón 'Search Projects' esté disponible y hacer clic
        search_projects_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_search_project"))
        )
        search_projects_button.click()

        # Confirmar que se ha redirigido a la página de búsqueda de proyectos
        assert "search_projects" in self.driver.current_url, "Freelancer not redirected to search projects page."     

        # Paso 3: Ingresar el nombre del cliente en la barra de búsqueda
        search_projects_page = SearchProjectsPage(self.driver)

        search_bar = WebDriverWait(self.driver, 10).until( 
            EC.visibility_of_element_located((By.ID, "search_project_bar"))
        )
        search_bar.send_keys("testclient4321")

        search_projects_page.submit_search()

        project_titles = search_projects_page.get_project_titles()
        assert "Proyecto de Prueba" in project_titles, "Project 'Proyecto de Prueba' not found in search results."
