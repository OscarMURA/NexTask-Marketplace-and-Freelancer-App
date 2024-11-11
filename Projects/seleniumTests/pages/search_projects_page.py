from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchProjectsPage:
    def __init__(self, driver):
        self.driver = driver

    def click_on_project(self, project_id):
        
        project_card = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='card h-100' and @onclick=\"window.location.href='/en/projects/project/view/{project_id}/'\"]"))
        )
        project_card.click()
