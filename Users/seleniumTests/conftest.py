import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="class")  # Cambiar a "class" para hacer el fixture de clase
def setup(request):
    service = Service(executable_path="C:/chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    driver.maximize_window()
    request.cls.driver = driver  # Asignar driver a request.cls
    yield
    driver.quit() 
