from selenium.webdriver.common.by import By

class TaskDetailFreelancerPage:
    def __init__(self, driver):
        self.driver = driver

    # Método para obtener el título de la tarea
    def get_task_title(self):
        return self.driver.find_element(By.CSS_SELECTOR, "h3.text-24").text

    # Método para obtener la descripción de la tarea
    def get_task_description(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".quill-content").text

    # Método para obtener la fecha de vencimiento de la tarea
    def get_task_due_date(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".form-control.readonly-field").text

    # Método para hacer clic en el botón "Edit" de la tarea
    def click_edit_task(self):
        edit_button = self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
        edit_button.click()

    # Método para hacer clic en "Back" a la página de hito
    def click_back_to_milestone(self):
        back_button = self.driver.find_element(By.CSS_SELECTOR, ".w-btn-danger-lg")
        back_button.click()
