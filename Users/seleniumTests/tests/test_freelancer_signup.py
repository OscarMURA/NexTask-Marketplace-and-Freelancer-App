import pytest
from pages.freelancer_signup_page import FreelancerSignUpPage
@pytest.mark.selenium
@pytest.mark.usefixtures("setup")
class TestFreelancerSignUp:
    
    def test_freelancer_sign_up_success(self):
        signup_page = FreelancerSignUpPage(self.driver)
        signup_page.go_to_signup_page()
        signup_page.fill_signup_form(
            username="testfreelancer",
            email="freelancer@example.com",
            first_name="Test",
            last_name="Freelancer",
            password="SecurePassword123",
            country="USA",
            city="New York",
            address="123 Main St",
            phone="123456789"
        )
        signup_page.submit_form()
        assert signup_page.is_redirected_to_work_experience()

    def test_freelancer_sign_up_missing_fields(self):
        signup_page = FreelancerSignUpPage(self.driver)
        signup_page.go_to_signup_page()

        signup_page.fill_signup_form(
            username="",
            email="freelancer@example.com",
            first_name="",
            last_name="Freelancer",
            password="SecurePassword123",
            country="USA",
            city="",
            address="",
            phone="123456789"
        )
        signup_page.submit_form()
        assert signup_page.is_error_message_displayed("This field is required")
    
    def test_freelancer_sign_up_password_mismatch(self):
        signup_page = FreelancerSignUpPage(self.driver)
        signup_page.go_to_signup_page()

        signup_page.fill_signup_form(
            username="testfreelancer",
            email="freelancer@example.com",
            first_name="Test",
            last_name="Freelancer",
            password1="SecurePassword123",
            password2="DifferentPassword",
            country="USA",
            city="New York",
            address="123 Main St",
            phone="123456789"
        )
        signup_page.submit_form()
        assert signup_page.is_error_message_displayed("The two password fields didn’t match.")
