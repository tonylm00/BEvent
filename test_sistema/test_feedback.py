
from selenium import webdriver
from selenium.webdriver.common.by import By



class TestScritturaRecensione():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_scritturaRecensione(self):
        self.driver.get("http://127.0.0.1:5000/area_organizzatore")
        self.driver.set_window_size(1621, 1241)
        self.driver.find_element(By.LINK_TEXT, "Dettagli Evento").click()
        self.driver.find_element(By.CSS_SELECTOR, "#rating-65982b4f8439ad64aed7a4ca > label:nth-child(2)").click()
        self.driver.find_element(By.ID, "review-title").click()
        self.driver.find_element(By.ID, "review-title").send_keys("Fiori Magnifici")
        self.driver.find_element(By.ID, "review-body").click()
        self.driver.find_element(By.CSS_SELECTOR, "body").click()
        self.driver.find_element(By.ID, "review-body").click()
        self.driver.find_element(By.ID, "review-body").send_keys(
            "Ho scelto questo servizio colpito dalle foto dei fiori i quali dal vivo erano belli come in foto")
        self.driver.find_element(By.ID, "submit-review").click()

