from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_login_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/login/")

    def fill_login_form(self, username, password):
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)

    def submit_form(self):
        self.driver.find_element(By.ID, "submit-btn").click()

    def is_redirected_to_home(self):
        return "/Home-Freelancer/" in self.driver.current_url or "/home-Client/" in self.driver.current_url

    def is_error_message_displayed(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".alert-danger").is_displayed()
