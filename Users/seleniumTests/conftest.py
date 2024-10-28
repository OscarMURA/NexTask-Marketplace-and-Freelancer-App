import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def setup(request):
    service = Service(executable_path="C:/chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()
