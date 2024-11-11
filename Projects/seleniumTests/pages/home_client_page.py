from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomeClientPage:
    def __init__(self, driver):
        self.driver = driver

    def find_delete_button(self, project_id):
        # Esperamos a que el botón de eliminación del proyecto esté visible y disponible para hacer clic
        delete_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"delete-project-{project_id}"))
        )
        return delete_button

    def click_remove_button(self, project_id):
        # Esperamos a que el modal correspondiente esté visible
        modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, f"RemoveModal{project_id}"))
        )
        
        # Ahora buscamos el botón "Remove" dentro del modal usando su ID
        remove_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"remove-btn-{project_id}"))
        )
        
        # Hacemos clic en el botón de eliminación
        remove_button.click()

    def get_no_projects_message(self):
        # Esperamos a que el mensaje "No projects available." esté visible
        no_projects_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'No projects available.')]"))
        )
        return no_projects_messageç
    
    def click_view_project_button(self):
        # Esperamos hasta que el botón 'View Project' sea clickeable
        view_project_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "view_project_btt"))
        )
        view_project_button.click()

    def click_manage_applications_button(self):
        # Esperamos hasta que el botón 'Manage Applications Freelancer' sea clickeable
        manage_applications_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "manage_freelancer_applications_btn"))
        )
        manage_applications_button.click()