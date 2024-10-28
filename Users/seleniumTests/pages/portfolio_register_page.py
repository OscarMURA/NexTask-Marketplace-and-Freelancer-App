from selenium.webdriver.common.by import By

class PortfolioRegisterPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_portfolio_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/portfolio/register/")
        
    def fill_portfolio_form(self, project_name, project_description, project_url):
        self.driver.find_element(By.NAME, "project_name").send_keys(project_name)
        self.driver.find_element(By.NAME, "project_description").send_keys(project_description)
        self.driver.find_element(By.NAME, "project_url").send_keys(project_url)

    def submit_form(self):
        self.driver.find_element(By.ID, "submit-btn").click()
