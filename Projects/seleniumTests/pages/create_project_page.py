from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class CreateProjectPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'http://127.0.0.1:8000/en/projects/createProject/'

    # Selectores de elementos
    TITLE_INPUT = (By.ID, "id_title")
    START_DATE_INPUT = (By.ID, "id_start_date")
    DUE_DATE_INPUT = (By.ID, "id_due_date")
    BUDGET_INPUT = (By.ID, "id_budget")
    CATEGORY_SELECT = (By.ID, "id_category")
    DESCRIPTION_INPUT = (By.CLASS_NAME, "ql-editor")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Métodos
    def load(self):
        self.driver.get(self.url)

    def set_title(self, title):
        self.driver.find_element(*self.TITLE_INPUT).send_keys(title)

    def set_start_date(self, start_date):
        self.driver.find_element(*self.START_DATE_INPUT).send_keys(start_date)

    def set_due_date(self, due_date):
        self.driver.find_element(*self.DUE_DATE_INPUT).send_keys(due_date)

    def set_budget(self, budget):
        self.driver.find_element(*self.BUDGET_INPUT).send_keys(budget)

    def select_category(self, category_name):
        category_dropdown = Select(self.driver.find_element(*self.CATEGORY_SELECT))
        category_dropdown.select_by_visible_text(category_name)

    def set_description(self, description):
        self.driver.find_element(*self.DESCRIPTION_INPUT).send_keys(description)

    def submit_form(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
