from selenium.webdriver.common.by import By

class SearchFreelancerPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'http://127.0.0.1:8000/en/projects/search_freelancer/'

    # Selectores de elementos
    SEARCH_INPUT = (By.NAME, "search")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Métodos
    def load(self):
        self.driver.get(self.url)

    def search_freelancer(self, query):
        self.driver.find_element(*self.SEARCH_INPUT).send_keys(query)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
