from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://127.0.0.1:8000/en/users/login/"  # Make sure this is the correct URL for your login page
        self.email_input = (By.NAME, "username")  # Update this to match your login form's username field
        self.password_input = (By.NAME, "password")  # Update this to match your password field
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")  # Update to match your submit button

    def load(self):
        self.driver.get(self.url)

    def login(self, username, password):
        self.driver.find_element(*self.email_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.submit_button).click()
