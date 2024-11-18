import pytest
from pages.login_page import LoginPage
from pages.home_client_page import HomeClientPage
from pages.project_detail_client import ProjectDetailClientPage
from pages.milestone_edit_page import MilestoneEditPage

@pytest.mark.usefixtures("setup")
@pytest.mark.selenium
class TestMilestoneEdit:
    @pytest.mark.run(order=13)
    def test_edit_milestone(self):
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        login_page.login(username="testclient123", password="SecurePassword123")

        self.driver.get("http://127.0.0.1:8000/en/projects/home-Client/")
        assert "home-Client" in self.driver.current_url, f"Expected to be on Home-Client, but found {self.driver.current_url}."

        home_client_page = HomeClientPage(self.driver)
        home_client_page.click_view_project_button()

        project_detail_page = ProjectDetailClientPage(self.driver)
        assert "project/1/" in self.driver.current_url, f"Expected to be on project details page, but found {self.driver.current_url}."

        project_detail_page.click_edit_milestone_button()

        milestone_edit_page = MilestoneEditPage(self.driver)
        assert "/projects/milestones/1/edit/" in self.driver.current_url, f"Expected to be on milestone edit page, but found {self.driver.current_url}."


        milestone_edit_page.fill_milestone_edit_form(
            title="Nuevo Título del Hito",
            start_date="01/01/2025",
            due_date="01/01/2026",
            category="Content-Writing",
            description="Descripción actualizada del hito"
        )

        milestone_edit_page.submit_form()

        assert "project/1/" in self.driver.current_url, f"Expected to be redirected to project details page, but found {self.driver.current_url}."
