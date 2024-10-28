from selenium.webdriver.common.by import By

class ProjectDetailPage:
    def __init__(self, driver):
        self.driver = driver
        self.url_template = 'http://127.0.0.1:8000/en/projects/{}/'  # Cambiar según la estructura de URLs

    # Selectores de elementos
    EDIT_BUTTON = (By.XPATH, "//a[contains(text(), 'Edit Project')]")
    DELETE_BUTTON = (By.XPATH, "//button[contains(text(), 'Remove')]")

    # Métodos
    def load(self, project_id):
        self.driver.get(self.url_template.format(project_id))

    def click_edit(self):
        self.driver.find_element(*self.EDIT_BUTTON).click()

    def delete_project(self):
        self.driver.find_element(*self.DELETE_BUTTON).click()
