# Generated by Selenium IDE

from selenium import webdriver
from selenium.webdriver.common.by import By


class TestTestRegistraFornitori:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()

    def test_testRegistraFornitori(self):
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1552, 840)
        self.driver.find_element(By.CSS_SELECTOR, "lord-icon").click()
        self.driver.find_element(By.NAME, "email").click()
        self.driver.find_element(By.ID, "register").click()
        self.driver.find_element(By.ID, "dropdown").click()
        dropdown = self.driver.find_element(By.ID, "dropdown")
        dropdown.find_element(By.XPATH, "//option[. = 'Fornitore']").click()
        self.driver.find_element(By.CSS_SELECTOR, "#registrazione > button").click()
        self.driver.find_element(By.NAME, "nome").click()
        self.driver.find_element(By.NAME, "nome").send_keys("Lucia")
        self.driver.find_element(By.NAME, "cognome").send_keys("Manfuso")
        self.driver.find_element(By.NAME, "data_di_nascita").send_keys("0002-06-15")
        self.driver.find_element(By.NAME, "data_di_nascita").send_keys("0020-06-15")
        self.driver.find_element(By.NAME, "data_di_nascita").send_keys("0200-06-15")
        self.driver.find_element(By.NAME, "data_di_nascita").send_keys("2000-06-15")
        self.driver.find_element(By.NAME, "nome_utente").send_keys("Luci Music")
        self.driver.find_element(By.CSS_SELECTOR, ".field-container:nth-child(3) > input:nth-child(1)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".field-container:nth-child(3) > input:nth-child(1)").send_keys(
            "l.manfuso@gmail.com")
        self.driver.find_element(By.ID, "password").send_keys("Ciao.123")
        self.driver.find_element(By.ID, "cpassword").send_keys("Ciao.123")
        self.driver.find_element(By.NAME, "telefono").click()
        self.driver.find_element(By.NAME, "telefono").send_keys("3471528692")
        self.driver.find_element(By.NAME, "citta").click()
        self.driver.find_element(By.NAME, "citta").send_keys("Roma")
        self.driver.find_element(By.NAME, "via").click()
        self.driver.find_element(By.NAME, "via").send_keys("Via Picerno 17")
        self.driver.find_element(By.NAME, "eventi_max_giornaliero").click()
        self.driver.find_element(By.NAME, "eventi_max_giornaliero").send_keys("1")
        self.driver.find_element(By.NAME, "isLocation").click()
        dropdown = self.driver.find_element(By.NAME, "isLocation")
        dropdown.find_element(By.XPATH, "//option[. = 'No']").click()
        self.driver.find_element(By.NAME, "p_iva").click()
        self.driver.find_element(By.NAME, "p_iva").click()
        self.driver.find_element(By.NAME, "p_iva").send_keys("08145296685")
        self.driver.find_element(By.ID, "descrizione").click()
        self.driver.find_element(By.ID, "descrizione").send_keys("Sono una cantante di musica lirica")
        self.driver.find_element(By.NAME, "regione").click()
        dropdown = self.driver.find_element(By.NAME, "regione")
        dropdown.find_element(By.XPATH, "//option[. = 'Lazio']").click()
        self.driver.find_element(By.CSS_SELECTOR, ".button").click()
