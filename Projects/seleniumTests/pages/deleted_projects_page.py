from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

class DeletedProjectsPage:
    def __init__(self, driver):
        self.driver = driver

    def get_deleted_project_titles(self):
        deleted_project_titles = []
        project_titles_elements = self.driver.find_elements(By.XPATH, "//p[@class='mb-0 text-primary']")
        
        for element in project_titles_elements:
            deleted_project_titles.append(element.text)
        
        return deleted_project_titles

    def click_delete_permanently_button(self, project_id):
        # Esperamos a que el botón de "Delete Permanently" esté visible y disponible para hacer clic
        delete_permanently_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"delete-permanently-btn-{project_id}"))
        )
        # Hacemos clic en el botón
        delete_permanently_button.click()

        # Esperamos que la alerta sea visible y la aceptamos
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert.accept()  # Aceptar la alerta (confirmar la eliminación permanente)

    def click_restore_button(self, project_id):
        # Esperamos a que el botón "Restore" esté visible y disponible para hacer clic
        restore_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"restore-btn-{project_id}"))
        )
        # Hacemos clic en el botón de restauración
        restore_button.click()