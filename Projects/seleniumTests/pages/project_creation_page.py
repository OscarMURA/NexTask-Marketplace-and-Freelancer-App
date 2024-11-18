from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProjectCreationPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'http://127.0.0.1:8000/en/projects/createProject/'
        self.wait = WebDriverWait(driver, 10)

    def go_to_project_creation_page(self):
        self.driver.get(self.url)

    def fill_project_form(self, title, start_date, due_date, budget, category, description):
        self.driver.find_element(By.NAME, "title").send_keys(title)
        self.driver.find_element(By.NAME, "start_date").send_keys(start_date)
        self.driver.find_element(By.NAME, "due_date").send_keys(due_date)
        self.driver.find_element(By.NAME, "budget").send_keys(budget)
        self.driver.find_element(By.NAME, "category").send_keys(category)
        description_element = self.driver.find_element(By.CLASS_NAME, "ql-editor")
        description_element.click()
        description_element.send_keys(description)

    def submit_form(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def is_redirected_to_home_client(self):
        # Verificar redirección al home-Client
        return self.wait.until(EC.url_contains("home-Client"))
