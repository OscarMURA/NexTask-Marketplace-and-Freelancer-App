from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TaskCreationPage:
    def __init__(self, driver, milestone_id):
        self.driver = driver
        self.url = f'http://127.0.0.1:8000/en/projects/milestone/{milestone_id}/add_task/'
        self.wait = WebDriverWait(driver, 10)

    def fill_task_form(self, title, start_date, due_date, priority, status, description):
        self.driver.find_element(By.ID, "id_title").send_keys(title)
        self.driver.find_element(By.ID, "id_start_date").send_keys(start_date)
        self.driver.find_element(By.ID, "id_due_date").send_keys(due_date)
        
       
        self.driver.find_element(By.ID, "id_priority").send_keys(priority)
        self.driver.find_element(By.ID, "id_status").send_keys(status)

       
        description_element = self.driver.find_element(By.CLASS_NAME, "ql-editor")
        description_element.click()
        description_element.send_keys(description)

    def submit_form(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def is_task_created_successfully(self, milestone_id):
       
        return f"/milestone/{milestone_id}/" in self.driver.current_url
