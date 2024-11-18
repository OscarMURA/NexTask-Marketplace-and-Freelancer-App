import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.client_signup_page import ClientSignUpPage
from pages.profile_settings_page import ProfileSettingsPage

@pytest.mark.selenium
@pytest.mark.usefixtures("setup")
class TestClientProfileFlow:

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

        # Navegar a la configuración del perfil
        profile_settings_page = ProfileSettingsPage(self.driver)
        profile_settings_page.go_to_profile_settings()

        # Validar que la página se cargue correctamente
        assert profile_settings_page.is_on_profile_settings_page(), "Profile settings page not loaded."

        # Actualización del perfil
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

        # Esperar a que el modal de confirmación aparezca
        modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "updateModal"))
        )
        assert modal.is_displayed(), "Update confirmation modal did not appear."

        # Validar que el mensaje en el modal es correcto
        modal_message = self.driver.find_element(By.CSS_SELECTOR, "#updateModal .modal-body").text
        assert "Your profile information has been updated successfully." in modal_message, "Update message mismatch."

        print("Test de actualización del perfil completado con éxito.")
