from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ModalInteraction:
    def __init__(self, driver):
        self.driver = driver

    def confirm_deletion(self):
        """
        Confirma la eliminación del proyecto dentro del modal.
        """
        # Esperar que el modal de confirmación sea visible y hacer clic en el botón 'Remove'
        remove_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Remove']"))
        )
        remove_button.click()
