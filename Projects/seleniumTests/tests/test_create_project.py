import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.create_project_page import CreateProjectPage

@pytest.mark.order(2)
class TestCreateProject:

    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def test_create_project(self):
        driver = self.driver

        # Navegar a la página de Crear Proyecto
        create_project_page = CreateProjectPage(driver)
        create_project_page.load()

        # Rellenar el formulario de creación de proyecto
        create_project_page.set_title("Test Project Title")
        create_project_page.set_start_date("10/10/2024")  # dd/mm/yyyy
        create_project_page.set_due_date("10/11/2024")    # dd/mm/yyyy
        create_project_page.set_budget("1000")
        create_project_page.select_category("Web Development")
        create_project_page.set_description("This is a test project description.")

        # Enviar el formulario
        create_project_page.submit_form()

        # Verificar si el proyecto fue creado exitosamente
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Project created successfully')]"))
        )
        assert success_message.is_displayed()

    def teardown_method(self, method):
        self.driver.quit()
