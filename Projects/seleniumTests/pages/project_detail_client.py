from selenium.webdriver.common.by import By

class ProjectDetailClientPage:
    def __init__(self, driver):
        self.driver = driver

    # Locator for the "Freelancer List in the project" button
    FREELANCERS_IN_PROJECT_BUTTON = (By.ID, "freelancers_in_project_btt")

    # Method to click on the "Freelancer List in the project" button
    def click_freelancers_in_project_button(self):
        freelancers_button = self.driver.find_element(*self.FREELANCERS_IN_PROJECT_BUTTON)
        freelancers_button.click()
