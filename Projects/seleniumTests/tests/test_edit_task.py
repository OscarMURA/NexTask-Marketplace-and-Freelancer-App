import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.home_client_page import HomeClientPage
from pages.project_detail_page import ProjectDetailPage  # Importación corregida
from pages.task_edit_page import TaskEditPage

@pytest.mark.usefixtures("setup")
class TestEditTask:
    @pytest.mark.run(order=14)
    def test_edit_task(self):
        # Paso 1: Iniciar sesión como cliente
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        login_page.login(username="testclient123", password="SecurePassword123")

        # Paso 2: Navegar al Home-Client
        self.driver.get("http://127.0.0.1:8000/en/projects/home-Client/")
        assert "home-Client" in self.driver.current_url, f"Expected to be on Home-Client, but found {self.driver.current_url}."

        # Paso 3: Ir a los detalles del proyecto
        home_client_page = HomeClientPage(self.driver)
        home_client_page.click_view_project_button()

        # Paso 4: Verificar que estamos en los detalles del proyecto
        project_detail_page = ProjectDetailPage(self.driver)  # Clase corregida
        assert "project/1/" in self.driver.current_url, f"Expected to be on project details page, but found {self.driver.current_url}."

        # Paso 5: Ir a los detalles del hito
        project_detail_page.click_view_milestone_button()

        # Paso 6: Verificar que estamos en los detalles del hito
        assert "milestone/1/" in self.driver.current_url, f"Expected to be on milestone details page, but found {self.driver.current_url}."

        # Paso 7: Hacer clic en el botón de "Editar Tarea" directamente con Selenium
        self.driver.find_element(By.ID, "edit_task_btt").click()

        # Paso 8: Verificar que estamos en la página de edición de la tarea
        assert "task/1/edit/" in self.driver.current_url, f"Expected to be on task edit page, but found {self.driver.current_url}."

        # Paso 9: Continuar con la edición de la tarea
        task_edit_page = TaskEditPage(self.driver)

        # Llenar el formulario de edición de tareas
        task_edit_page.fill_task_edit_form(
            title="Nueva Tarea Editada",
            due_date="15/12/2024",
            description="Descripción actualizada para la tarea editada."
        )

        # Paso 10: Guardar los cambios
        task_edit_page.submit_form()

        # Paso 11: Verificar que se redirige correctamente a la página de detalles del hito
        assert "milestone/1/" in self.driver.current_url, f"Expected to be redirected to milestone details page, but found {self.driver.current_url}."
