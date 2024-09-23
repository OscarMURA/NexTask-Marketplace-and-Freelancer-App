# Documentación de Pruebas de Modelos

## Tabla de Setup (Fixtures)

| Nombre del Setup (Fixture) | Descripción                                      |
|----------------------------|--------------------------------------------------|
| `user`                     | Crea un usuario para las pruebas.                |
| `freelancer_profile`       | Crea un perfil de freelancer asociado al usuario. |

## Tabla de Pruebas

| Nombre de la Prueba                               | Nombre del Setup     | Entradas                                                                                                                       | Salidas Esperadas                                                 |
|---------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| `test_freelancer_profile_creation`                | `freelancer_profile` | N/A                                                                                                                           | El perfil se crea correctamente con los valores especificados.   |
| `test_freelancer_skills`                          | `freelancer_profile` | `skill = Skill.objects.create(name="Python")`                                                                                | El perfil tiene la habilidad "Python".                           |
| `test_freelancer_education`                       | `freelancer_profile` | `(freelancer_profile, "MIT", "Bachelor of Computer Science", "2015-09-01", "2019-06-30", "Computer Science program")`      | El objeto de educación se crea correctamente.                   |
| `test_freelancer_work_experience`                 | `freelancer_profile` | `(freelancer_profile, "Tech Corp", "Software Engineer", "2020-01-01", "2022-12-31", "Worked on backend development")`      | El objeto de experiencia laboral se crea correctamente.          |
| `test_freelancer_certifications`                  | `freelancer_profile` | `(freelancer_profile, "AWS Certified Solutions Architect", "Amazon", "2021-05-01", None, "AWS Solutions Architect certification")` | El objeto de certificación se crea correctamente.               |
| `test_freelancer_portfolio`                       | `freelancer_profile` | `(freelancer_profile, "http://portfolio.example.com", "My personal portfolio")`                                             | El objeto de portafolio se crea correctamente.                  |
| `test_client_profile_creation`                     | N/A                  | `(user, "Tech Co.", "http://techco.com", "US", "San Francisco", "123456789", "1234 Tech St.")`                             | El perfil de cliente se crea correctamente.                     |
| `test_unique_skill_creation`                       | N/A                  | `"Django"`                                                                                                                   | Se lanza una excepción al intentar crear una habilidad duplicada. |
| `test_freelancer_skill_assignment`                 | N/A                  | `(freelancer_profile, ["Python", "Django"])`                                                                               | Las habilidades se asocian correctamente al perfil.             |
| `test_freelancer_profile_optional_fields`          | N/A                  | `(user, "US")`                                                                                                             | Se guarda correctamente, los campos opcionales permanecen vacíos. |
| `test_client_profile_optional_fields`              | N/A                  | `(user, "Test Company", "US")`                                                                                              | Se guarda correctamente, los campos opcionales permanecen vacíos. |
| `test_freelancer_profile_skills`                   | N/A                  | `(user, ["Python", "Django", "JavaScript"])`                                                                              | Se asocian correctamente 3 habilidades al perfil.               |
| `test_freelancer_profile_missing_required_fields`  | `user`               | `(user, "New York", "123456789", "1234 Freelance Ave")`                                                                     | Se lanza un ValueError por campo obligatorio faltante.           |
| `test_freelancer_profile_phone_length`             | `freelancer_profile` | `"1" * 21`                                                                                                                  | Se lanza una ValidationError por longitud de teléfono excesiva.  |
| `test_freelancer_profile_cascade_delete`           | `freelancer_profile` | `(freelancer_profile, "Tech Corp", "Software Engineer", "2020-01-01", "2022-12-31")`                                       | Se verifica que la experiencia laboral se elimine al borrar el perfil. |
| `test_skill_reverse_relation`                       | N/A                  | `(skill, freelancer_profile)`                                                                                                | La relación inversa se verifica correctamente.                   |
| `test_freelancer_profile_update`                   | `freelancer_profile` | `"Los Angeles"`                                                                                                             | Se actualiza correctamente el perfil.                            |


# Documentación de Pruebas de Vista

## Tabla de Setup (Fixtures)

| Nombre del Setup (Fixture) | Descripción                                      |
|----------------------------|--------------------------------------------------|
| `client`                   | Cliente de pruebas de Django para simular solicitudes HTTP. |

## Tabla de Pruebas

| Nombre de la Prueba                                      | Nombre del Setup | Entradas                                                                                                                                                           | Salidas Esperadas                                                    |
|----------------------------------------------------------|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| `test_freelancer_signup_view_get`                       | `client`         | N/A                                                                                                                                                               | Código de respuesta 200 y uso de la plantilla `Users/freelancer_signup.html`. |
| `test_freelancer_signup_view_post`                      | `client`         | `{'username': 'testfreelancer', 'email': 'freelancer@test.com', 'password1': 'testpassword123', 'password2': 'testpassword123', 'first_name': 'Test', 'last_name': 'Freelancer', 'country': 'CO', 'city': 'TestCity', 'phone': '123456789', 'address': 'Test Address'}` | Código de respuesta 302 y creación de usuario y perfil de freelancer.   |
| `test_freelancer_signup_password_mismatch`              | `client`         | `{'username': 'testfreelancer2', 'email': 'freelancer2@test.com', 'password1': 'password123', 'password2': 'differentpassword123', 'first_name': 'Test', 'last_name': 'Freelancer', 'country': 'CO', 'city': 'TestCity', 'phone': '123456789', 'address': 'Test Address'}` | Código de respuesta 200 y mensaje de error de coincidencia de contraseñas. |
| `test_freelancer_signup_duplicate_username`              | `client`         | `{'username': 'testfreelancer', 'email': 'freelancer@test.com', 'password1': 'password123@', 'password2': 'password123@', 'first_name': 'Test', 'last_name': 'Freelancer', 'country': 'CO', 'city': 'TestCity', 'phone': '123456789', 'address': 'Test Address'}` | Código de respuesta 200 y mensaje de error por nombre de usuario duplicado. |
| `test_freelancer_signup_missing_required_field`          | `client`         | `{'username': '', 'email': 'freelancer@test.com', 'password1': 'password123', 'password2': 'password123', 'first_name': 'Test', 'last_name': 'Freelancer', 'country': 'CO', 'city': 'TestCity', 'phone': '123456789', 'address': 'Test Address'}` | Código de respuesta 200 y mensaje de error por campo obligatorio faltante. |
| `test_freelancer_signup_invalid_email`                   | `client`         | `{'username': 'testfreelancer3', 'email': 'invalid-email', 'password1': 'password123', 'password2': 'password123', 'first_name': 'Test', 'last_name': 'Freelancer', 'country': 'CO', 'city': 'TestCity', 'phone': '123456789', 'address': 'Test Address'}` | Código de respuesta 200 y mensaje de error por correo electrónico no válido. |
| `test_freelancer_signup_form_display`                    | `client`         | N/A                                                                                                                                                               | Código de respuesta 200 y `form` en el contexto de la respuesta.  |
| `test_freelancer_signup_form_invalid_data`               | `client`         | `{'username': '', 'email': 'invalid-email', 'password1': 'password123', 'password2': 'differentpassword', 'first_name': '', 'last_name': '', 'country': '', 'city': '', 'phone': '', 'address': ''}` | Código de respuesta 200 y errores en el contexto del formulario.   |
| `test_login_redirect_to_welcome`                         | `client`         | `{'username': 'testlogin', 'password': 'password123'}`                                                                                                         | Código de respuesta 200 y redirección a la página de bienvenida.   |
| `test_freelancer_signup_successful_with_extra_fields`   | `client`         | `{'username': 'extra_fields_freelancer', 'email': 'extra@test.com', 'password1': 'password123!', 'password2': 'password123!', 'first_name': 'Extra', 'last_name': 'Fields', 'country': 'CO', 'city': 'ExtraCity', 'phone': '987654321', 'address': 'Extra Address'}` | Código de respuesta 302 y creación de usuario y perfil.            |
| `test_freelancer_signup_form_required_fields`            | `client`         | `{'username': 'required_fields_test', 'email': '', 'password1': '', 'password2': '', 'first_name': 'Test', 'last_name': 'Required', 'country': 'CO', 'city': 'RequiredCity', 'phone': '123456789', 'address': 'Required Address'}` | Código de respuesta 200 y mensaje de error por campos requeridos.   |
| `test_freelancer_signup_success_with_valid_email`        | `client`         | `{'username': 'valid_email_freelancer', 'email': 'validemail@test.com', 'password1': 'password123!', 'password2': 'password123!', 'first_name': 'Valid', 'last_name': 'Email', 'country': 'CO', 'city': 'ValidCity', 'phone': '123456789', 'address': 'Valid Address'}` | Código de respuesta 302 y creación de usuario.                     |
| `test_portfolio_register_view_get`                       | `client`         | N/A                                                                                                                                                               | Código de respuesta 200 y uso de la plantilla `Users/portfolio_register.html`. |
| `test_freelancer_signup_missing_fields`                  | `client`         | `{'username': 'required_fields_test', 'email': 'freelancer@test.com', 'password1': 'password123', 'password2': 'password123'}`                                   | Código de respuesta 200 y mensaje de error por campos faltantes.    |
| `test_welcome_view`                                      | `client`         | N/A                                                                                                                                                               | Código de respuesta 200 y uso de la plantilla `Users/welcome.html`. |
| `test_freelancer_signup_username_max_length`             | `client`         | `{'username': 'a' * 151, 'email': 'freelancer@test.com', 'password1': 'password123', 'password2': 'password123'}`                                                  | Código de respuesta 200 y mensaje de error por longitud excesiva.   |
| `test_freelancer_signup_optional_fields`                  | `client`         | `{'username': 'testoptional', 'email': 'optional@test.com', 'password1': 'StrongPassword123!', 'password2': 'StrongPassword123!', 'first_name': 'Test', 'last_name': 'Freelancer', 'country': 'CO', 'city': 'TestCity'}` | Código de respuesta 302 y creación de usuario.                     |
| `test_login_redirect_by_user_type`                        | `client`         | N/A                                                                                                                                                               | Redirección correcta según el tipo de usuario.                     |
| `test_logout_and_protected_view_access`                  | `client`         | N/A                                                                                                                                                               | Código de respuesta 302 al intentar acceder a vista protegida tras logout. |
| `test_freelancer_profile_update`                          | `client`         | `{'username': 'freelancer_update', 'email': 'update@test.com', 'first_name': 'Updated', 'last_name': 'Freelancer', 'city': 'NewCity', 'country': 'CO', 'phone': '987654321', 'address': 'Updated Address'}` | Código de respuesta 200 y actualización exitosa del perfil.        |

# Documentación de Formularios

## Tabla de Setup (Fixtures)

| Nombre del Setup (Fixture) | Descripción                                      |
|----------------------------|--------------------------------------------------|
| N/A                        | No se utilizan setups específicos en estas pruebas. |

## Tabla de Formularios

| Nombre del Formulario                               | Descripción                                               | Campos                                                                                                                                                 |
|----------------------------------------------------|----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `UserSignUpForm`                                   | Formulario base para el registro de usuarios.           | `username`, `email`, `first_name`, `last_name`, `password1`, `password2`, `country`, `city`, `phone`, `address`                                    |
| `FreelancerSignUpForm`                             | Formulario para el registro de freelancers.             | Hereda de `UserSignUpForm` + validación del campo `phone` y creación del perfil de freelancer al guardar.                                            |
| `ClientSignUpForm`                                 | Formulario para el registro de clientes.                | Hereda de `UserSignUpForm` + campos adicionales: `company_name`, `company_website`. Crea un perfil de cliente al guardar.                             |
| `CertificationFormSet`                             | Formset para las certificaciones de un freelancer.      | `certification_name`, `issuing_organization`, `issue_date`, `expiration_date`, `short_description`.                                                  |
| `PortfolioFormSet`                                 | Formset para el portafolio de un freelancer.           | `url`, `description`.                                                                                                                                 |
| `EducationFormSet`                                 | Formset para la educación de un freelancer.             | `institution_name`, `degree_obtained`, `start_date`, `end_date`, `description`.                                                                      |
| `WorkExperienceFormSet`                            | Formset para la experiencia laboral de un freelancer.   | `company_name`, `position`, `start_date`, `end_date`, `description`.                                                                                |
| `SkillsForm`                                       | Formulario para gestionar habilidades de un freelancer.  | `skills`, `new_skill`. Permite agregar nuevas habilidades si no están en la base de datos.                                                            |
| `LanguageForm`                                     | Formulario para seleccionar múltiples idiomas.           | `languages` (campos de selección múltiple).                                                                                                           |

## Notas

- Cada formulario y formset está diseñado para manejar la entrada de datos de usuarios en el contexto de la creación y gestión de perfiles de freelancers y clientes.
- Se aplican validaciones específicas en algunos formularios, como la longitud del teléfono y la coincidencia de contraseñas en el `FreelancerSignUpForm`.
