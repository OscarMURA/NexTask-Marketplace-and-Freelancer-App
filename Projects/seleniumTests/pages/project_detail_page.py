from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProjectDetailPage:
    def __init__(self, driver):
        self.driver = driver

    def click_apply_button(self):
        
        apply_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Apply to Project']"))
        )
        apply_button.click()
