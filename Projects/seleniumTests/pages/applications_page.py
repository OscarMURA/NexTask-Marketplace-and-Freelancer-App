from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ApplicationsPage:
    def __init__(self, driver):
        self.driver = driver

    def click_accept_button(self):
        accept_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "accetp_applFreelancer_btt"))
        )
        accept_button.click()

    def get_applications_text(self):
        freelancer_name_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'testfreelancer123')]"))
        )
        return freelancer_name_element.text
    
    def click_reject_button(self):
        reject_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "denied_applFreelancer_btt"))
        )
        reject_button.click()
