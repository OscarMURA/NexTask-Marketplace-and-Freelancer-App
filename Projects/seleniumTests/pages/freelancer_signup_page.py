from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FreelancerSignUpPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_signup_page(self):
        # Navegar a la página de registro del freelancer
        self.driver.get("http://127.0.0.1:8000/en/users/signup/freelancer/")

    def fill_signup_form(self, username, first_name, last_name, phone, email, country, city, address, password, confirm_password):
        # Completar el formulario de registro
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "first_name").send_keys(first_name)
        self.driver.find_element(By.ID, "last_name").send_keys(last_name)
        self.driver.find_element(By.ID, "phone").send_keys(phone)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "id_country").send_keys(country)
        self.driver.find_element(By.ID, "city").send_keys(city)
        self.driver.find_element(By.ID, "address").send_keys(address)
        self.driver.find_element(By.ID, "password1").send_keys(password)
        self.driver.find_element(By.ID, "password2").send_keys(confirm_password)

    def submit_form(self):
        
        self.driver.find_element(By.ID, "submit-btn").click()
