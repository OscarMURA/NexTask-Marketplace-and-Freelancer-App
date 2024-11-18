import pytest
from selenium.webdriver.common.by import By
from pages.home_freelancer_page import HomeFreelancerPage
from pages.project_detail_freelancer_page import ProjectDetailFreelancerPage
from pages.milestone_detail_freelancer_page import MilestoneDetailFreelancerPage
from pages.task_detail_freelancer_page import TaskDetailFreelancerPage
from pages.login_page import LoginPage

@pytest.mark.usefixtures("setup")
@pytest.mark.selenium
class TestFreelancerNavigation:
    @pytest.mark.run(order=10)
    def test_project_milestone_task_navigation(self):
        # Paso 1: Login como freelancer
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        login_page.login(username="testfreelancer123", password="SecurePassword123")    

        # Paso 2: Ir al Home-Freelancer
        self.driver.get("http://127.0.0.1:8000/en/users/Home-Freelancer/")
        assert "Home-Freelancer" in self.driver.current_url, "Freelancer not redirected to home-Freelancer."

        # Paso 3: Hacer clic en el botón de "Ver Proyecto"
        home_freelancer_page = HomeFreelancerPage(self.driver)
        home_freelancer_page.click_view_project_button()

        # Paso 4: Asegurarse que estamos en la página de detalles del proyecto
        project_detail_page = ProjectDetailFreelancerPage(self.driver)
        assert "project/1/" in self.driver.current_url, "Not redirected to project details page."

        # Paso 5: Hacer clic en el hito dentro del proyecto
        project_detail_page.click_milestone_image()

        # Paso 6: Asegurarse que estamos en la página de detalles del hito
        milestone_detail_page = MilestoneDetailFreelancerPage(self.driver)
        assert "milestone/1/details/" in self.driver.current_url, "Not redirected to milestone details page."

        # Paso 7: Hacer clic en la tarea dentro del hito
        milestone_detail_page.click_task()

        # Paso 8: Asegurarse que estamos en la página de detalles de la tarea
        task_detail_page = TaskDetailFreelancerPage(self.driver)
        assert "task/1/" in self.driver.current_url, "Not redirected to task details page."
