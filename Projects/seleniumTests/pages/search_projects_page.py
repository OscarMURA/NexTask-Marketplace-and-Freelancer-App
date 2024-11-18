from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchProjectsPage:
    def __init__(self, driver):
        self.driver = driver

    def click_on_project(self, project_id):
        
        project_card = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='card h-100' and @onclick=\"window.location.href='/en/projects/project/view/{project_id}/'\"]"))
        )
        project_card.click()
    def submit_search(self):
        
        search_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "search_project_button"))
        )
        search_button.click()

    # Método opcional si necesitas interactuar con la barra de búsqueda
    def enter_search_query(self, query):
        # Esperar a que la barra de búsqueda esté visible y rellenarla con la consulta
        search_bar = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "search_project_bar"))
        )
        search_bar.send_keys(query)

    # Método para obtener los títulos de los proyectos mostrados
    def get_project_titles(self):
        # Esperar hasta que los proyectos estén visibles
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title"))
        )
        project_titles = self.driver.find_elements(By.CLASS_NAME, "card-title")
        return [title.text for title in project_titles]
    def get_project_titles(self):
        # Obtener los títulos de los proyectos visibles
        titles = []
        projects = self.driver.find_elements(By.CSS_SELECTOR, ".card-title")
        for project in projects:
            titles.append(project.text)
        return titles

