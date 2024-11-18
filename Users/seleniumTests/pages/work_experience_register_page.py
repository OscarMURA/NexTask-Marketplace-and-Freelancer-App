from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WorkExperienceRegisterPage:
    def __init__(self, driver):
        self.driver = driver

    def fill_work_experience_form(self, form_index, title, company, location, start_date, end_date, description):
        base = f'work_experiences-{form_index}-'
        self.driver.find_element(By.NAME, f"{base}title").send_keys(title)
        self.driver.find_element(By.NAME, f"{base}company").send_keys(company)
        self.driver.find_element(By.NAME, f"{base}location").send_keys(location)
        self.driver.find_element(By.NAME, f"{base}start_date").send_keys(start_date)
        self.driver.find_element(By.NAME, f"{base}end_date").send_keys(end_date)
        self.driver.find_element(By.NAME, f"{base}description").send_keys(description)

    def submit_form(self):
        self.driver.find_element(By.ID, "next_btt").click()

    def is_freelancer_in_results(self, username):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "dynamic-form"))
        )
        results = self.driver.find_elements(By.CLASS_NAME, "dynamic-form")
        return any(username in result.text for result in results)

    def no_results_found(self):
        try:
            return self.driver.find_element(By.CLASS_NAME, "no-results").is_displayed()
        except NoSuchElementException:
            return False
