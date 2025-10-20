import os, time, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# === Configuración del navegador (sin cambios) ===

def initialize_driver():
    """
    Inicializa un driver de Firefox con configuración compatible con sistemas snap.
    """
    options = webdriver.FirefoxOptions()
    snap_tmp = os.path.expanduser("~/snap/firefox/common/tmp")
    os.makedirs(snap_tmp, exist_ok=True)
    os.environ["TMPDIR"] = snap_tmp
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(1024, 768)
    return driver

def close_driver(driver):
    """Cierra el navegador."""
    driver.quit()

@pytest.fixture(scope="module")
def driver():
    """
    Fixture que crea y cierra automáticamente el navegador.
    """
    d = initialize_driver()
    yield d
    close_driver(d)

# === Test de interfaz para Notepad ===

def test_create_notepad_via_web_form(driver):
    """
    Flujo de prueba para Notepad:
    1. Abrir la página de login e iniciar sesión.
    2. Navegar a la página para crear una nueva nota.
    3. Rellenar el título y el cuerpo de la nota.
    4. Pulsar el botón de guardar.
    5. Comprobar que la nueva nota aparece en la lista.
    """
    # 1️ Iniciar sesión
    driver.get("http://localhost:5000/login")
    time.sleep(1)
    
    driver.find_element(By.NAME, "email").send_keys("user1@example.com")
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    # 2️ Navegar a la página de creación
    driver.get("http://localhost:5000/notepad/create")
    time.sleep(1)

    # 3️ Rellenar el formulario de la nota
    title_input = driver.find_element(By.NAME, "title")
    title_input.clear()
    title_input.send_keys("Mi Nota con Selenium")

    body_input = driver.find_element(By.NAME, "body")
    body_input.clear()
    body_input.send_keys("Este es el cuerpo de la nota automatizada.")
    
    # 4️ Enviar el formulario
    submit_button = driver.find_element(By.NAME, "submit")
    submit_button.click()
    time.sleep(1)

    # 5️ Verificar que la nueva nota aparece en la lista
    # Primero, nos aseguramos de que hemos sido redirigidos a la página correcta
    assert "/notepad" in driver.current_url, "No se redirigió a la página de la lista de notas."
    
    page_source = driver.page_source
    assert "Mi Nota con Selenium" in page_source, "La nueva nota no se muestra en la lista."
    assert "Este es el cuerpo de la nota automatizada." in page_source
