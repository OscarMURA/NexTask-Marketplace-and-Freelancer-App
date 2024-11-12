from selenium.webdriver.common.by import By

class HomeFreelancerPage:
    def __init__(self, driver):
        self.driver = driver

    def click_search_projects_button(self):
      
        search_button = self.driver.find_element(By.ID, "id_search_project")
        search_button.click()
        
    
