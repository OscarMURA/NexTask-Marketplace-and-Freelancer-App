from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TaskEditPage:
    def __init__(self, driver):
        self.driver = driver

    # Locators
    TITLE_FIELD = (By.ID, "id_title")
    DUE_DATE_FIELD = (By.ID, "id_due_date")
    DESCRIPTION_FIELD = (By.CSS_SELECTOR, ".ql-editor")  # Quill editor
    SAVE_BUTTON = (By.ID, "saveChanges_btt")

    def fill_task_edit_form(self, title, due_date, description):
        """Completar el formulario de edición de tareas."""
        title_field = self.driver.find_element(*self.TITLE_FIELD)
        title_field.clear()
        title_field.send_keys(title)

        due_date_field = self.driver.find_element(*self.DUE_DATE_FIELD)
        due_date_field.clear()
        due_date_field.send_keys(due_date)
        due_date_field.send_keys(Keys.TAB)  # Asegurar la actualización del campo

        description_field = self.driver.find_element(*self.DESCRIPTION_FIELD)
        self.driver.execute_script("arguments[0].innerHTML = '';", description_field)  # Limpiar contenido existente
        description_field.send_keys(description)

    def submit_form(self):
        """Enviar el formulario."""
        self.driver.find_element(*self.SAVE_BUTTON).click()
