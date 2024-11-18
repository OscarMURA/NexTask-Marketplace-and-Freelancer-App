from selenium.webdriver.common.by import By

class MilestoneDetailPage:
    def __init__(self, driver):
        self.driver = driver

   
    EDIT_TASK_BUTTON = (By.ID, "edit_task_btt")

    def click_edit_task_button(self):
       
        self.driver.find_element(*self.EDIT_TASK_BUTTON).click()
