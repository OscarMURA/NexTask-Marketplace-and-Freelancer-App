from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_login_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/login/")

    def login(self, username, password):
        self.driver.find_element(By.ID, "id_username").send_keys(username)
        self.driver.find_element(By.ID, "id_password").send_keys(password)
        self.driver.find_element(By.ID, "submit-btn").click()
