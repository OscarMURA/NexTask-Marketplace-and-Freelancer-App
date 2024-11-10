from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MilestoneCreationPage:
    def __init__(self, driver, project_id):
        self.driver = driver
        self.project_id = project_id
        self.url = f"http://127.0.0.1:8000/en/projects/project/{project_id}/add_milestone/"
        
        self.wait = WebDriverWait(driver, 10)

    def go_to_milestone_creation_page(self):
        self.driver.get(self.url)

    def fill_milestone_form(self, title, start_date, due_date, category, description):
        # Completar el campo de título del hito
        title_field = self.wait.until(EC.presence_of_element_located((By.ID, "id_title")))
        title_field.send_keys(title)

        # Completar la fecha de inicio
        start_date_field = self.driver.find_element(By.ID, "id_start_date")
        start_date_field.send_keys(start_date)

        # Completar la fecha de vencimiento
        due_date_field = self.driver.find_element(By.ID, "id_due_date")
        due_date_field.send_keys(due_date)

        # Seleccionar la categoría
        category_select = self.driver.find_element(By.ID, "id_category")
        category_select.send_keys(category)

        # Rellenar el campo de descripción usando el editor Quill
        description_field = self.driver.find_element(By.CLASS_NAME, "ql-editor")
        description_field.click()
        description_field.send_keys(description)

    def submit_form(self):
        # Enviar el formulario
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

    def is_milestone_created_successfully(self, project_id):
        # Confirmación de redirección al detalle del proyecto
        expected_url = f"/project/{project_id}/"
        return self.wait.until(EC.url_contains(expected_url))
