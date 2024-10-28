import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.task_page import TaskPage

@pytest.mark.order(4)
class TestCreateTask:

    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def test_create_task(self):
        driver = self.driver

        # Navegar a la página de Crear Tarea
        task_page = TaskPage(driver)
        task_page.load()

        # Rellenar el formulario de creación de tarea
        task_page.set_title("Test Task")
        task_page.set_due_date("15/12/2024")  # dd/mm/yyyy
        task_page.set_description("This is a test task description.")
        task_page.select_milestone("Test Milestone")

        # Enviar el formulario
        task_page.submit_form()

        # Verificar si la tarea fue creada exitosamente
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Task created successfully')]"))
        )
        assert success_message.is_displayed()

    def teardown_method(self, method):
        self.driver.quit()
