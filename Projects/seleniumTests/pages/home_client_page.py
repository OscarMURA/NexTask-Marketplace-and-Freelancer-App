from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomeClientPage:
    def __init__(self, driver):
        self.driver = driver
        self.VIEW_PROJECT_BUTTON = (By.ID, "view_project_btt")

    def find_delete_button(self, project_id):
       
        delete_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"delete-project-{project_id}"))
        )
        return delete_button

    def click_remove_button(self, project_id):
        
        modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, f"RemoveModal{project_id}"))
        )
        
      
        remove_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"remove-btn-{project_id}"))
        )
        
       
        remove_button.click()

    def get_no_projects_message(self):
       
        no_projects_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'No projects available.')]"))
        )
        return no_projects_messageç
    
    def click_view_project_button(self):
      
        view_project_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.VIEW_PROJECT_BUTTON)
        )
        view_project_button.click()

    def click_manage_applications_button(self):
      
        manage_applications_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "manage_freelancer_applications_btn"))
        )
        manage_applications_button.click()
        
    def click_search_freelancer_button(self):
        search_freelancer_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "search_freelancer_btt"))
        )
        search_freelancer_button.click()