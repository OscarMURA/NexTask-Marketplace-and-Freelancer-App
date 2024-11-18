import pytest
from selenium.webdriver.common.by import By
from pages.client_signup_page import ClientSignUpPage
from pages.profile_settings_page import ProfileSettingsPage

@pytest.mark.usefixtures("setup")
class TestClientFullFlow:
    
    def test_register_and_update_profile(self):
        # Registro del cliente
        signup_page = ClientSignUpPage(self.driver)
        signup_page.go_to_signup_page()
        signup_page.fill_signup_form(
            username="testclient123",
            email="client123@example.com",
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
        assert signup_page.is_redirected_to_client_home(), "User registration failed"
        
        # Actualización del perfil
        profile_settings_page = ProfileSettingsPage(self.driver)
        profile_settings_page.go_to_profile_settings()
        profile_settings_page.fill_profile_form(
            username="testclient123",
            email="clientnewemail@example.com",
            first_name="NewName",
            last_name="NewClient",
            company_name="UpdatedCompany",
            company_website="http://updatedcompany.com",
            country="Canada",
            city="Toronto",
            phone="987654321",
            address="123 New Address"
        )
        profile_settings_page.submit_form()
        assert profile_settings_page.is_profile_updated(), "Profile update failed"
