from selenium.webdriver.common.by import By

class ClientSignUpPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_signup_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/signup/client/")

    def fill_signup_form(self, username, email, first_name, last_name, password, country, city, phone, company_name, company_website):
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "first_name").send_keys(first_name)
        self.driver.find_element(By.NAME, "last_name").send_keys(last_name)
        self.driver.find_element(By.NAME, "password1").send_keys(password)
        self.driver.find_element(By.NAME, "password2").send_keys(password)
        self.driver.find_element(By.NAME, "country").send_keys(country)
        self.driver.find_element(By.NAME, "city").send_keys(city)
        self.driver.find_element(By.NAME, "phone").send_keys(phone)
        self.driver.find_element(By.NAME, "company_name").send_keys(company_name)
        self.driver.find_element(By.NAME, "company_website").send_keys(company_website)

    def submit_form(self):
        self.driver.find_element(By.ID, "submit-btn").click()

    def is_redirected_to_client_home(self):
        return "/home-Client" in self.driver.current_url

    def is_error_message_displayed(self, error_message):
        return error_message in self.driver.page_source
