from selenium.webdriver.common.by import By

class EducationRegisterPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_education_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/education/register/")
        
    def fill_education_form(self, institution_name, degree, field_of_study, start_year, end_year):
        self.driver.find_element(By.NAME, "institution_name").send_keys(institution_name)
        self.driver.find_element(By.NAME, "degree").send_keys(degree)
        self.driver.find_element(By.NAME, "field_of_study").send_keys(field_of_study)
        self.driver.find_element(By.NAME, "start_year").send_keys(start_year)
        self.driver.find_element(By.NAME, "end_year").send_keys(end_year)

    def submit_form(self):
        self.driver.find_element(By.ID, "submit-btn").click()
