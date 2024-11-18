from selenium.webdriver.common.by import By

class MilestoneDetailFreelancerPage:
    def __init__(self, driver):
        self.driver = driver

    TASK_ELEMENT = (By.ID, "task_detail_on_click")

    def click_task(self):
        task_element = self.driver.find_element(*self.TASK_ELEMENT)
        task_element.click()

    # Method to get the milestone title
    def get_milestone_title(self):
        return self.driver.find_element(By.CSS_SELECTOR, "h3.text-24").text

    # Method to get the milestone description
    def get_milestone_description(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".quill-content").text

    # Method to get the milestone category
    def get_milestone_category(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".form-control.readonly-field").text


