from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProjectDetailPage:
    def __init__(self, driver):
        self.driver = driver

    # Locator para el botón de aplicar al proyecto
    APPLY_BUTTON = (By.XPATH, "//button[text()='Apply to Project']")
    
    # Locator para el botón de ver hito
    VIEW_MILESTONE_BUTTON = (By.ID, "view-milestone-btt")

    def click_apply_button(self):
        """Haz clic en el botón de 'Aplicar al Proyecto'."""
        apply_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.APPLY_BUTTON)
        )
        apply_button.click()

    def click_view_milestone_button(self):
        """Haz clic en el botón de 'Ver Hito'."""
        milestone_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.VIEW_MILESTONE_BUTTON)
        )
        milestone_button.click()
