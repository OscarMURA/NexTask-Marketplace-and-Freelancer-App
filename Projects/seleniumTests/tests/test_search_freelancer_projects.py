import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.home_client_page import HomeClientPage
from pages.search_freelancer_page import SearchFreelancerPage

@pytest.mark.usefixtures("setup")
@pytest.mark.selenium
class TestSearchFreelancer:
    @pytest.mark.run(order=7)
    def test_search_freelancer_from_home(self):
        # Paso 1: Login como cliente
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()

        # Completar el formulario de login con las credenciales del cliente
        login_page.login(username="testclient123", password="SecurePassword123")

        # Redirigir a Home-Client
        self.driver.get("http://127.0.0.1:8000/en/projects/home-Client/")
        assert "home-Client" in self.driver.current_url, "Client not redirected to home-Client."

        # Paso 2: Hacer clic en el botón "View Project" del proyecto específico
        home_client_page = HomeClientPage(self.driver)

        # Esperar hasta que el botón 'View Project' esté disponible y hacer clic
        view_project_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "view_project_btt"))
        )
        view_project_button.click()

        # Paso 3: Hacer clic en "Search Freelancer"
        search_freelancer_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "search_freelancer_btt"))
        )
        search_freelancer_button.click()

        # Paso 4: Ingresar el nombre del freelancer en la barra de búsqueda
        search_freelancer_page = SearchFreelancerPage(self.driver)

        # Esperar a que el campo de búsqueda sea visible y rellenarlo
        search_bar = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "seacrh_bar_freelancer"))
        )
        search_bar.send_keys("testfreelancer321")

        # Paso 5: Confirmar que el resultado de búsqueda aparece correctamente
        search_freelancer_page.submit_search()

        # Esperar a que aparezca el nombre del freelancer buscado en los resultados
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h5[contains(text(), 'testfreelancer321')]"))
        )
        freelancer_name = self.driver.find_element(By.XPATH, "//h5[contains(text(), 'testfreelancer321')]")
        assert freelancer_name.text == "testfreelancer321", "Freelancer not found in the search results."
