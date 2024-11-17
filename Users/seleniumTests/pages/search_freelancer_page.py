from selenium.webdriver.common.by import By

class SearchFreelancerPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_search_freelancer_page(self):
        self.driver.get("http://127.0.0.1:8000/en/users/search/")

    def search_freelancer_by_username(self, username):
        search_field = self.driver.find_element(By.NAME, "keyword")
        search_field.clear()
        search_field.send_keys(username)
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

    def search_freelancer_by_skill(self, skill):
        skill_field = self.driver.find_element(By.NAME, "skills")
        skill_field.clear()
        skill_field.send_keys(skill)
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

    def is_freelancer_in_results(self, username):
        return username in self.driver.page_source

    def no_results_found(self):
        return "No freelancers found" in self.driver.page_source
