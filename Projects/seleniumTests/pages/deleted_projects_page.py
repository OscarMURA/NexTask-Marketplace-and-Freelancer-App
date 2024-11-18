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
        delete_permanently_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"delete-permanently-btn-{project_id}"))
        )
        delete_permanently_button.click()

        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert.accept()  

    def click_restore_button(self, project_id):
       
        restore_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"restore-btn-{project_id}"))
        )
       
        restore_button.click()