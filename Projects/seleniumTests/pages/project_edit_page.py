from selenium.webdriver.common.by import By

class ProjectEditPage:
    def __init__(self, driver):
        self.driver = driver

    # Locators for the project edit form fields
    TITLE_FIELD = (By.ID, "id_title")
    START_DATE_FIELD = (By.ID, "id_start_date")
    DUE_DATE_FIELD = (By.ID, "id_due_date")
    BUDGET_FIELD = (By.ID, "id_budget")
    CATEGORY_FIELD = (By.ID, "id_category")
    DESCRIPTION_FIELD = (By.CSS_SELECTOR, ".ql-editor")  # Updated to target the Quill editor's class

    SAVE_BUTTON = (By.ID, "save_changes_btt")

    def fill_project_edit_form(self, title, start_date, due_date, budget, category, description):
        # Fill in the title
        self.driver.find_element(*self.TITLE_FIELD).clear()
        self.driver.find_element(*self.TITLE_FIELD).send_keys(title)

        # Fill in the start date
        self.driver.find_element(*self.START_DATE_FIELD).clear()
        self.driver.find_element(*self.START_DATE_FIELD).send_keys(start_date)

        # Fill in the due date
        self.driver.find_element(*self.DUE_DATE_FIELD).clear()
        self.driver.find_element(*self.DUE_DATE_FIELD).send_keys(due_date)

        # Fill in the budget
        self.driver.find_element(*self.BUDGET_FIELD).clear()
        self.driver.find_element(*self.BUDGET_FIELD).send_keys(budget)

        # Select the category
        category_select = self.driver.find_element(*self.CATEGORY_FIELD)
        for option in category_select.find_elements(By.TAG_NAME, 'option'):
            if option.text == category:
                option.click()
                break

        # Fill in the description (Quill editor)
        description_field = self.driver.find_element(*self.DESCRIPTION_FIELD)
        description_field.clear()  # Clear the existing content
        description_field.send_keys(description)  # Enter the new description

    def submit_form(self):
        # Submit the form
        self.driver.find_element(*self.SAVE_BUTTON).click()
