from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ClientSignUpPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'http://127.0.0.1:8000/en/users/signup/client/'  
        self.wait = WebDriverWait(driver, 10)

    def go_to_signup_page(self):
        self.driver.get(self.url)

    def fill_signup_form(self, username, email, first_name, last_name, company_name, country, city, password):
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "first_name").send_keys(first_name)
        self.driver.find_element(By.ID, "last_name").send_keys(last_name)
        self.driver.find_element(By.ID, "company_name").send_keys(company_name)
        self.driver.find_element(By.NAME, "country").send_keys(country)  # country es un select
        self.driver.find_element(By.ID, "city").send_keys(city)
        self.driver.find_element(By.ID, "password1").send_keys(password)
        self.driver.find_element(By.ID, "password2").send_keys(password)

    def submit_form(self):
        self.driver.find_element(By.ID, "submit-btn").click()

    def is_redirected_to_client_home(self):
        # Espera a que el redireccionamiento suceda y valida si está en la página de inicio del cliente
        return self.wait.until(EC.url_contains("home-Client"))
