from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MilestoneEditPage:
    def __init__(self, driver):
        self.driver = driver
        self.TITLE_FIELD = (By.ID, "id_title")
        self.START_DATE_FIELD = (By.ID, "id_start_date")
        self.DUE_DATE_FIELD = (By.ID, "id_due_date")
        self.CATEGORY_FIELD = (By.ID, "id_category")
        self.DESCRIPTION_FIELD = (By.CSS_SELECTOR, ".ql-editor")  # Quill editor
        self.SAVE_BUTTON = (By.ID, "save_changes_btt")

    def fill_milestone_edit_form(self, title, start_date, due_date, category, description):
        # Rellenar los campos del formulario de edición
        self.driver.find_element(*self.TITLE_FIELD).clear()
        self.driver.find_element(*self.TITLE_FIELD).send_keys(title)

        self.driver.find_element(*self.START_DATE_FIELD).clear()
        self.driver.find_element(*self.START_DATE_FIELD).send_keys(start_date)

        self.driver.find_element(*self.DUE_DATE_FIELD).clear()
        self.driver.find_element(*self.DUE_DATE_FIELD).send_keys(due_date)

        # Seleccionar la categoría
        category_select = self.driver.find_element(*self.CATEGORY_FIELD)
        for option in category_select.find_elements(By.TAG_NAME, 'option'):
            if option.text == category:
                option.click()
                break

        # Rellenar la descripción (Quill editor)
        description_field = self.driver.find_element(*self.DESCRIPTION_FIELD)
        description_field.clear()  # Limpiar contenido actual
        description_field.send_keys(description)  # Ingresar nueva descripción

    def submit_form(self):
        # Enviar el formulario
        self.driver.find_element(*self.SAVE_BUTTON).click()
