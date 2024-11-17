from selenium.webdriver.common.by import By

class CertificationRegisterPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_certification_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/certification/register/")
        
    def fill_certification_form(self, certification_name, institution, issue_date, expiration_date):
        self.driver.find_element(By.NAME, "certification_name").send_keys(certification_name)
        self.driver.find_element(By.NAME, "institution").send_keys(institution)
        self.driver.find_element(By.NAME, "issue_date").send_keys(issue_date)
        self.driver.find_element(By.NAME, "expiration_date").send_keys(expiration_date)

    def submit_form(self):
        self.driver.find_element(By.ID, "submit-btn").click()
