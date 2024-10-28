import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.search_freelancer_page import SearchFreelancerPage

@pytest.mark.order(5)
class TestSearchFreelancer:

    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def test_search_freelancer(self):
        driver = self.driver

        # Navegar a la página de Búsqueda de Freelancers
        search_freelancer_page = SearchFreelancerPage(driver)
        search_freelancer_page.load()

        # Realizar la búsqueda
        search_freelancer_page.search_freelancer("Web Developer")

        # Verificar si la búsqueda tuvo éxito
        results_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Freelancers found')]"))
        )
        assert results_message.is_displayed()

    def teardown_method(self, method):
        self.driver.quit()
