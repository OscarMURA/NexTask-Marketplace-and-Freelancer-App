class MilestonePage:
    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get("http://127.0.0.1:8000/en/milestones/create/")  # Update with the correct URL

    def set_title(self, title):
        title_field = self.driver.find_element(By.ID, "id_title")
        title_field.clear()
        title_field.send_keys(title)

    def set_due_date(self, due_date):
        due_date_field = self.driver.find_element(By.ID, "id_due_date")
        due_date_field.clear()
        due_date_field.send_keys(due_date)

    def set_description(self, description):
        description_field = self.driver.find_element(By.ID, "id_description")
        description_field.clear()
        description_field.send_keys(description)

    def submit_form(self):
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
