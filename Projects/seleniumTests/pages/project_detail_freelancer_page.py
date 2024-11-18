from selenium.webdriver.common.by import By

class ProjectDetailFreelancerPage:
    def __init__(self, driver):
        self.driver = driver

    # Método para obtener el título del proyecto
    def get_project_title(self):
        return self.driver.find_element(By.CSS_SELECTOR, "h3.text-24").text

    MILESTONE_IMAGE = (By.ID, "on_click_milestone")

    # Method to click on the milestone image
    def click_milestone_image(self):
        milestone_image = self.driver.find_element(*self.MILESTONE_IMAGE)
        milestone_image.click()

    # Método para obtener la descripción del proyecto
    def get_project_description(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".quill-content").text

    # Método para obtener la categoría del proyecto
    def get_project_category(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".form-control.readonly-field").text
