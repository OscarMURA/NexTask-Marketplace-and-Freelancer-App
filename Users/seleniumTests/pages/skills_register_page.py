from selenium.webdriver.common.by import By

class SkillsRegisterPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_skills_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/skills/register/")
        
    def fill_skills_form(self, skill_name, skill_level):
        self.driver.find_element(By.NAME, "skill_name").send_keys(skill_name)
        self.driver.find_element(By.NAME, "skill_level").send_keys(skill_level)

    def submit_form(self):
        self.driver.find_element(By.ID, "submit-btn").click()
