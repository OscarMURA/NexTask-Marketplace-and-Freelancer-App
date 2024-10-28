import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.mark.order(1)
class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)  # Implicit wait to handle delays

    def test_login(self):
        driver = self.driver

        # Step 1: Load the login page
        login_page = LoginPage(driver)
        login_page.load()

        # Step 2: Log in with test credentials (Update with valid credentials)
        login_page.login("testClient", "client_password")  # Make sure these credentials are valid

        # Step 3: Verify successful login by checking for an element that is displayed after login
        try:
            # Wait for a specific element that only appears after login
            dashboard_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h3[text()='Dashboard']"))  # Adjust this to a unique element on the dashboard
            )
            self.assertTrue(dashboard_element.is_displayed())  # Assert that the element is displayed

        except Exception as e:
            self.fail(f"Login test failed: {e}")

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
