import pytest
from pages.client_signup_page import ClientSignUpPage

@pytest.mark.usefixtures("setup")
class TestClientSignUp:
    
    def test_client_sign_up_success(self):
        signup_page = ClientSignUpPage(self.driver)
        signup_page.go_to_signup_page()
        signup_page.fill_signup_form(
            username="testclient",
            email="client@example.com",
            first_name="Test",
            last_name="Client",
            password="SecurePassword123",
            country="USA",
            city="Los Angeles",
            phone="123456789",
            company_name="TestCompany",
            company_website="http://testcompany.com"
        )
        signup_page.submit_form()
        assert signup_page.is_redirected_to_client_home()

    def test_client_sign_up_invalid_email(self):
        signup_page = ClientSignUpPage(self.driver)
        signup_page.go_to_signup_page()

        signup_page.fill_signup_form(
            username="testclient",
            email="invalid-email",
            first_name="Test",
            last_name="Client",
            password="SecurePassword123",
            country="USA",
            city="Los Angeles",
            phone="123456789",
            company_name="TestCompany",
            company_website="http://testcompany.com"
        )
        signup_page.submit_form()
        assert signup_page.is_error_message_displayed("Enter a valid email address.")

    def test_client_sign_up_empty_fields(self):
        signup_page = ClientSignUpPage(self.driver)
        signup_page.go_to_signup_page()

        signup_page.fill_signup_form(
            username="",
            email="",
            first_name="Test",
            last_name="Client",
            password="SecurePassword123",
            country="USA",
            city="Los Angeles",
            phone="",
            company_name="",
            company_website=""
        )
        signup_page.submit_form()
        assert signup_page.is_error_message_displayed("This field is required")
