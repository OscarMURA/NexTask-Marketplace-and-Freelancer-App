from selenium.webdriver.common.by import By

class LanguageRegisterPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_language_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/languages/register/")
        
    def fill_language_form(self, language_name, proficiency_level):
        self.driver.find_element(By.NAME, "language_name").send_keys(language_name)
        self.driver.find_element(By.NAME, "proficiency_level").send_keys(proficiency_level)

    def submit_form(self):
        self.driver.find_element(By.ID, "submit-btn").click()
