import pytest
from pages.search_freelancer_page import SearchFreelancerPage
from pages.freelancer_signup_page import FreelancerSignUpPage
@pytest.mark.selenium
@pytest.mark.usefixtures("setup")
class TestSearchFreelancer:

    def test_search_freelancer_by_username(self):
        # Registrar un freelancer primero para la búsqueda
        signup_page = FreelancerSignUpPage(self.driver)
        signup_page.go_to_signup_page()
        signup_page.fill_signup_form(
            username="freelancersearch",
            email="freelancersearch@example.com",
            first_name="Freelancer",
            last_name="Search",
            password1="SecurePassword123",
            password2="SecurePassword123",
            country="USA",
            city="New York",
            address="123 Main St",
            phone="123456789"
        )
        signup_page.submit_form()

        # Buscar el freelancer registrado
        search_page = SearchFreelancerPage(self.driver)
        search_page.go_to_search_freelancer_page()
        search_page.search_freelancer_by_username("freelancersearch")

        # Verificar que el freelancer aparece en los resultados
        assert search_page.is_freelancer_in_results("freelancersearch")

    def test_search_freelancer_by_skill(self):
        search_page = SearchFreelancerPage(self.driver)
        search_page.go_to_search_freelancer_page()
        search_page.search_freelancer_by_skill("Python")

        # Verificar que el freelancer aparece en los resultados
        assert search_page.is_freelancer_in_results("Python")

    def test_search_freelancer_no_results(self):
        search_page = SearchFreelancerPage(self.driver)
        search_page.go_to_search_freelancer_page()
        search_page.search_freelancer_by_username("NonExistentFreelancer")

        # Verificar que no se encontraron resultados
        assert search_page.no_results_found()
