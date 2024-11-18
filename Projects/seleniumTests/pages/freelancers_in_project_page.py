from selenium.webdriver.common.by import By

class FreelancersInProjectPage:
    def __init__(self, driver):
        self.driver = driver

    # Locator for the freelancer's name in the project
    FREELANCER_NAME = (By.CLASS_NAME, "text-dark-200")

    # Method to get freelancer's name in the project
    def get_freelancer_name(self):
        return self.driver.find_element(*self.FREELANCER_NAME).text
