from selenium.webdriver.common.by import By  # Asegúrate de que esta línea esté presente

class DeletedProjectsPage:
    def __init__(self, driver):
        self.driver = driver

    def get_deleted_project_titles(self):
        
        deleted_project_titles = []
        project_titles_elements = self.driver.find_elements(By.XPATH, "//p[@class='mb-0 text-primary']")
        
        for element in project_titles_elements:
            deleted_project_titles.append(element.text)
        
        return deleted_project_titles
