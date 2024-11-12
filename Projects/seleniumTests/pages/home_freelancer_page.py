from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains  # Add this line
from selenium.webdriver.common.keys import Keys

class HomeFreelancerPage:
    def __init__(self, driver):
        self.driver = driver

    def click_search_projects_button(self):
      
        search_button = self.driver.find_element(By.ID, "id_search_project")
        search_button.click()
        
    VIEW_PROJECT_BUTTON = (By.ID, "view_project_btt")

    # Method to click on the "View Project" button
    def click_view_project_button(self):
        project_button = self.driver.find_element(*self.VIEW_PROJECT_BUTTON)
        project_button.click()
        
    
