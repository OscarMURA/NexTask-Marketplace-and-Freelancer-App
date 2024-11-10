# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def setup(request):
    # Inicia el servicio de ChromeDriver
    service = Service(executable_path="C:/chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    driver.maximize_window()
    request.cls.driver = driver  # Asigna el driver a la clase de prueba
    
    yield
    driver.quit()  # Cierra el driver después de las pruebas
