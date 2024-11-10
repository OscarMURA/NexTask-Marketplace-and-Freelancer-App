from selenium.webdriver.common.by import By

class WorkExperienceRegisterPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_work_experience_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/work-experience/register/")
        
    def fill_work_experience_form(self, title, company, location, start_date, end_date, description):
        self.driver.find_element(By.NAME, "title").send_keys(title)
        self.driver.find_element(By.NAME, "company").send_keys(company)
        self.driver.find_element(By.NAME, "location").send_keys(location)
        self.driver.find_element(By.NAME, "start_date").send_keys(start_date)
        self.driver.find_element(By.NAME, "end_date").send_keys(end_date)
        self.driver.find_element(By.NAME, "description").send_keys(description)

    def submit_form(self):
        self.driver.find_element(By.ID, "submit-btn").click()
    
    def is_on_work_experience_page(self):
        return "work-experience/register" in self.driver.current_url
