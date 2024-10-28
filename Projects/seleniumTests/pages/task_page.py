from selenium.webdriver.common.by import By

class TaskPage:
    def __init__(self, driver):
        self.driver = driver
        self.url_template = 'http://127.0.0.1:8000/en/projects/tasks/{}/'  # Cambiar según la URL de las tareas

    # Selectores de elementos
    TITLE_INPUT = (By.ID, "id_title")
    DUE_DATE_INPUT = (By.ID, "id_due_date")
    DESCRIPTION_INPUT = (By.CLASS_NAME, "ql-editor")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Métodos
    def load(self, task_id):
        self.driver.get(self.url_template.format(task_id))

    def set_title(self, title):
        self.driver.find_element(*self.TITLE_INPUT).send_keys(title)

    def set_due_date(self, due_date):
        self.driver.find_element(*self.DUE_DATE_INPUT).send_keys(due_date)

    def set_description(self, description):
        self.driver.find_element(*self.DESCRIPTION_INPUT).send_keys(description)

    def submit_form(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
