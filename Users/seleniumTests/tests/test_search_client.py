import pytest
from pages.search_client_page import SearchClientPage
from pages.client_signup_page import ClientSignUpPage
@pytest.mark.selenium
@pytest.mark.usefixtures("setup")
class TestSearchClient:

    def test_search_client_by_company_name(self):
        # Registrar un cliente primero para la búsqueda
        signup_page = ClientSignUpPage(self.driver)
        signup_page.go_to_signup_page()
        signup_page.fill_signup_form(
            username="clientsearch",
            email="clientsearch@example.com",
            first_name="Client",
            last_name="Search",
            password="SecurePassword123",
            country="USA",
            city="New York",
            phone="123456789",
            company_name="SearchCompany",
            company_website="http://searchcompany.com"
        )
        signup_page.submit_form()

        # Buscar el cliente registrado
        search_page = SearchClientPage(self.driver)
        search_page.go_to_search_client_page()
        search_page.search_client_by_company_name("SearchCompany")

        # Verificar que el cliente aparece en los resultados
        assert search_page.is_client_in_results("SearchCompany")

    def test_search_client_by_country(self):
        search_page = SearchClientPage(self.driver)
        search_page.go_to_search_client_page()
        search_page.search_client_by_country("USA")

        # Verificar que el cliente aparece en los resultados
        assert search_page.is_client_in_results("USA")

    def test_search_client_no_results(self):
        search_page = SearchClientPage(self.driver)
        search_page.go_to_search_client_page()
        search_page.search_client_by_company_name("NonExistentCompany")

        # Verificar que no se encontraron resultados
        assert search_page.no_results_found()
