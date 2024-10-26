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
        # Iniciar el flujo de registro de freelancer
        signup_page = FreelancerSignUpPage(self.driver)
        signup_page.go_to_signup_page()
        signup_page.fill_signup_form(
            username="testfreelancerflow",
            email="freelancerflow@example.com",
            first_name="Test",
            last_name="Flow",
            password="SecurePassword123",
            country="USA",
            city="New York",
            address="123 Main St",
            phone="123456789"
        )
        signup_page.submit_form()

        # Asegurarse de que se redirige a la página de experiencia laboral
        work_experience_page = WorkExperienceRegisterPage(self.driver)
        assert work_experience_page.is_on_work_experience_page()

        # Llenar el formulario de experiencia laboral
        work_experience_page.fill_work_experience_form(
            job_title="Software Engineer",
            company_name="Tech Corp",
            city="San Francisco",
            country="USA",
            description="Worked on various software projects",
            start_date="2020-01-01",
            end_date="2022-01-01"
        )
        work_experience_page.submit_form()

        # Validar que se completa correctamente y pasa a la siguiente sección
        assert work_experience_page.is_experience_saved()

        # Ir a la página de educación y llenar el formulario
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

        # Validar que la educación fue guardada
        assert education_page.is_education_saved()

        # Ir a la página de certificaciones y llenar el formulario
        certification_page = CertificationRegisterPage(self.driver)
        assert certification_page.is_on_certification_page()

        certification_page.fill_certification_form(
            certification_name="AWS Certified Developer",
            organization="Amazon",
            issue_date="2021-05-01",
            expiration_date="2024-05-01"
        )
        certification_page.submit_form()

        # Validar que la certificación fue guardada
        assert certification_page.is_certification_saved()

        # Ir a la página del portafolio y llenar el formulario
        portfolio_page = PortfolioRegisterPage(self.driver)
        assert portfolio_page.is_on_portfolio_page()

        portfolio_page.fill_portfolio_form(
            project_name="Web Development Project",
            description="Developed a full-stack web application",
            project_url="http://project-example.com"
        )
        portfolio_page.submit_form()

        # Validar que el portafolio fue guardado
        assert portfolio_page.is_portfolio_saved()

        # Ir a la página de idiomas y llenar el formulario
        language_page = LanguageRegisterPage(self.driver)
        assert language_page.is_on_language_page()

        language_page.fill_language_form(
            language="English",
            proficiency="Fluent"
        )
        language_page.submit_form()

        # Validar que los idiomas fueron guardados
        assert language_page.is_language_saved()

        # Ir a la página de habilidades y llenar el formulario
        skills_page = SkillsRegisterPage(self.driver)
        assert skills_page.is_on_skills_page()

        skills_page.fill_skills_form(
            skill="Python Programming",
            proficiency="Expert"
        )
        skills_page.submit_form()

        # Validar que las habilidades fueron guardadas
        assert skills_page.is_skills_saved()

        # Flujo completo exitoso
        print("Test del flujo completo de Freelancer completado con éxito.")
