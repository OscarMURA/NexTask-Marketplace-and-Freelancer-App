import pytest
from pages.freelancer_signup_page import FreelancerSignUpPage
from pages.work_experience_register_page import WorkExperienceRegisterPage
from pages.education_register_page import EducationRegisterPage
from pages.certification_register_page import CertificationRegisterPage
from pages.portfolio_register_page import PortfolioRegisterPage
from pages.language_register_page import LanguageRegisterPage
from pages.skills_register_page import SkillsRegisterPage

@pytest.mark.usefixtures("setup")
class TestFreelancerFullFlow:
    
    def test_freelancer_full_flow(self):
        signup_page = FreelancerSignUpPage(self.driver)
        signup_page.go_to_signup_page()
        signup_page.fill_signup_form(
            username="testfreelancerflow",
            email="freelancerflow@example.com",
            first_name="Test",
            last_name="Flow",
            password1="SecurePassword123",
            password2="SecurePassword123",
            country="USA",
            city="New York",
            address="123 Main St",
            phone="123456789"
        )
        signup_page.submit_form()

        work_experience_page = WorkExperienceRegisterPage(self.driver)
        assert work_experience_page.is_on_work_experience_page()

        work_experience_page.fill_work_experience_form(
            title="Software Engineer",
            company="Tech Corp",
            location="San Francisco",
            start_date="2020-01-01",
            end_date="2022-01-01",
            description="Worked on various software projects"
        )

        

        work_experience_page.submit_form()
        assert work_experience_page.is_experience_saved()

        education_page = EducationRegisterPage(self.driver)
        assert education_page.is_on_education_page()

        education_page.fill_education_form(
            school="University of Test",
            degree="Bachelor of Science",
            field_of_study="Computer Science",
            start_date="2015-01-01",
            end_date="2019-01-01"
        )
        education_page.submit_form()
        assert education_page.is_education_saved()

        certification_page = CertificationRegisterPage(self.driver)
        assert certification_page.is_on_certification_page()

        certification_page.fill_certification_form(
            certification_name="AWS Certified Developer",
            organization="Amazon",
            issue_date="2021-05-01",
            expiration_date="2024-05-01"
        )
        certification_page.submit_form()
        assert certification_page.is_certification_saved()

        portfolio_page = PortfolioRegisterPage(self.driver)
        assert portfolio_page.is_on_portfolio_page()

        portfolio_page.fill_portfolio_form(
            project_name="Web Development Project",
            description="Developed a full-stack web application",
            project_url="http://project-example.com"
        )
        portfolio_page.submit_form()
        assert portfolio_page.is_portfolio_saved()

        language_page = LanguageRegisterPage(self.driver)
        assert language_page.is_on_language_page()

        language_page.fill_language_form(
            language="English",
            proficiency="Fluent"
        )
        language_page.submit_form()
        assert language_page.is_language_saved()

        skills_page = SkillsRegisterPage(self.driver)
        assert skills_page.is_on_skills_page()

        skills_page.fill_skills_form(
            skill="Python Programming",
            proficiency="Expert"
        )
        skills_page.submit_form()
        assert skills_page.is_skills_saved()

        print("Test del flujo completo de Freelancer completado con éxito.")
