from selenium.webdriver.common.by import By

class ProfileSettingsPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_profile_settings(self):
        self.driver.get("http://127.0.0.1:8000/en/users/profileSettingsClient/")
    
    def fill_profile_form(self, username, email, first_name, last_name, company_name, company_website, country, city, phone, address):
        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "email").clear()
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "first_name").clear()
        self.driver.find_element(By.NAME, "first_name").send_keys(first_name)
        self.driver.find_element(By.NAME, "last_name").clear()
        self.driver.find_element(By.NAME, "last_name").send_keys(last_name)
        self.driver.find_element(By.NAME, "company_name").clear()
        self.driver.find_element(By.NAME, "company_name").send_keys(company_name)
        self.driver.find_element(By.NAME, "company_website").clear()
        self.driver.find_element(By.NAME, "company_website").send_keys(company_website)
        self.driver.find_element(By.NAME, "country").send_keys(country)
        self.driver.find_element(By.NAME, "city").clear()
        self.driver.find_element(By.NAME, "city").send_keys(city)
        self.driver.find_element(By.NAME, "phone").clear()
        self.driver.find_element(By.NAME, "phone").send_keys(phone)
        self.driver.find_element(By.NAME, "address").clear()
        self.driver.find_element(By.NAME, "address").send_keys(address)

    def submit_form(self):
        self.driver.find_element(By.ID, "submit-btn").click()

    def is_profile_updated(self):
        return "Profile updated successfully" in self.driver.page_source
