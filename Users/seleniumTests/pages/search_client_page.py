from selenium.webdriver.common.by import By

class SearchClientPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_search_client_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/search_clients/")

    def search_client_by_company_name(self, company_name):
        search_field = self.driver.find_element(By.NAME, "q")
        search_field.clear()
        search_field.send_keys(company_name)
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

    def search_client_by_country(self, country):
        country_field = self.driver.find_element(By.NAME, "country")
        country_field.clear()
        country_field.send_keys(country)
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

    def is_client_in_results(self, company_name):
        return company_name in self.driver.page_source

    def no_results_found(self):
        return "No clients found" in self.driver.page_source
