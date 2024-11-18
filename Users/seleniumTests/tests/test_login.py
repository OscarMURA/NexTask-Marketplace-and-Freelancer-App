import pytest
from pages.login_page import LoginPage
@pytest.mark.selenium
@pytest.mark.usefixtures("setup")
class TestLogin:
    
    def test_freelancer_login_success(self):
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        login_page.fill_login_form("testfreelancer", "SecurePassword123")
        login_page.submit_form()
        assert login_page.is_redirected_to_home()

    def test_client_login_success(self):
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        login_page.fill_login_form("testclient", "SecurePassword123")
        login_page.submit_form()
        assert login_page.is_redirected_to_home()

    def test_invalid_login(self):
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        login_page.fill_login_form("wronguser", "WrongPassword123")
        login_page.submit_form()
        assert "login" in self.driver.current_url

    def test_login_unregistered_account(self):
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()

        login_page.fill_login_form("nonexistentuser", "NonexistentPassword123")
        login_page.submit_form()
        assert "login" in self.driver.current_url
