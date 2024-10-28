import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.milestone_page import MilestonePage

@pytest.mark.order(3)
class TestCreateMilestone:

    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def test_create_milestone(self):
        driver = self.driver

        # Navegar a la página de Crear Hito
        milestone_page = MilestonePage(driver)
        milestone_page.load()

        # Rellenar el formulario de creación de hito
        milestone_page.set_title("Test Milestone")
        milestone_page.set_due_date("10/12/2024")  # dd/mm/yyyy
        milestone_page.set_description("This is a test milestone description.")

        # Enviar el formulario
        milestone_page.submit_form()

        # Verificar si el hito fue creado exitosamente
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Milestone created successfully')]"))
        )
        assert success_message.is_displayed()

    def teardown_method(self, method):
        self.driver.quit()
