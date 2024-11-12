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
