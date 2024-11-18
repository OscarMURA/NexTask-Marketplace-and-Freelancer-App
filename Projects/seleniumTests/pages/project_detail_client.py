from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProjectDetailClientPage:
    def __init__(self, driver):
        self.driver = driver
    


    # Locator for the "Freelancer List in the project" button
    FREELANCERS_IN_PROJECT_BUTTON = (By.ID, "freelancers_in_project_btt")

    # Method to click on the "Freelancer List in the project" button
    def click_freelancers_in_project_button(self):
        freelancers_button = self.driver.find_element(*self.FREELANCERS_IN_PROJECT_BUTTON)
        freelancers_button.click()
    

    # Method to get the project title
    def get_project_title(self):
        return self.driver.find_element(By.CSS_SELECTOR, "h3.text-24").text
    
    EDIT_MILESTONE_BUTTON = (By.ID, "edit_milestone_btt")

    def click_edit_milestone_button(self):
        try:
        # Esperar hasta que el botón sea clickeable y luego hacer clic
            edit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(self.EDIT_MILESTONE_BUTTON)
            )
            edit_button.click()
        except Exception as e:
            print(f"Error: {e}")
            raise
