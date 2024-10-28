from selenium.webdriver.common.by import By

class ManageApplicationsPage:
    def __init__(self, driver):
        self.driver = driver
        self.url_template = 'http://127.0.0.1:8000/en/projects/manage_applications/{}/'

    # Selectores de elementos
    ACCEPT_BUTTON = (By.XPATH, "//button[contains(text(), 'Accept')]")
    REJECT_BUTTON = (By.XPATH, "//button[contains(text(), 'Reject')]")

    # Métodos
    def load(self, project_id):
        self.driver.get(self.url_template.format(project_id))

    def accept_application(self, application_id):
        self.driver.find_element(By.ID, f"accept_{application_id}").click()

    def reject_application(self, application_id):
        self.driver.find_element(By.ID, f"reject_{application_id}").click()
