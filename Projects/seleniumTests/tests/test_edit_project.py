import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.home_client_page import HomeClientPage
from pages.project_edit_page import ProjectEditPage
from pages.project_detail_client import ProjectDetailClientPage

@pytest.mark.usefixtures("setup")
class TestProjectEdit:
    @pytest.mark.run(order=12)
    def test_edit_project(self):
        # Paso 1: Login como cliente
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        login_page.login(username="testclient123", password="SecurePassword123")

        # Paso 2: Ir al Home-Client
        self.driver.get("http://127.0.0.1:8000/en/projects/home-Client/")
        assert "home-Client" in self.driver.current_url, f"Expected to be on Home-Client, but found {self.driver.current_url}."

        # Paso 3: Hacer clic en el botón de 'Editar Proyecto' desde Home-Client
        home_client_page = HomeClientPage(self.driver)
        home_client_page.click_edit_project_button()

        # Paso 4: Asegurarse que estamos en la página de edición del proyecto
        project_edit_page = ProjectEditPage(self.driver)
        assert "edit/1/" in self.driver.current_url, f"Expected to be on project edit page, but found {self.driver.current_url}."

        # Paso 5: Completar el formulario de edición con nuevos datos
        project_edit_page.fill_project_edit_form(
            title="Nuevo Título de Proyecto",
            start_date="01/01/2025",
            due_date="01/01/2026",
            budget="3000",
            category="Content-Writing",
            description="Descripción actualizada del proyecto"
        )

        # Paso 6: Guardar los cambios
        project_edit_page.submit_form()

        # Paso 7: Verificar que hemos sido redirigidos a la página de detalles del proyecto
        assert "project/1/" in self.driver.current_url, f"Expected to be redirected to project details page, but found {self.driver.current_url}."

        # Paso 8: Verificar que los cambios se reflejan en la página de detalles del proyecto
        updated_title = self.driver.find_element(By.CSS_SELECTOR, "h3.text-24").text
        assert updated_title == "Nuevo Título de Proyecto", f"Expected 'Nuevo Título de Proyecto', but found {updated_title}."
