from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class KiemThuSauceDemo:

    def __init__(self):
        self.trinh_duyet = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.trinh_duyet.get("https://www.saucedemo.com/")
        self.trinh_duyet.maximize_window()

    def dang_nhap(self, ten_dang_nhap, mat_khau):
        self.trinh_duyet.find_element(By.ID, "user-name").send_keys(ten_dang_nhap)
        self.trinh_duyet.find_element(By.ID, "password").send_keys(mat_khau)
        self.trinh_duyet.find_element(By.ID, "login-button").click()
        WebDriverWait(self.trinh_duyet, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    def dang_nhap_thanh_cong(self):
        self.dang_nhap("standard_user", "secret_sauce")
        assert "inventory" in self.trinh_duyet.current_url
        print("Dang nhap thanh cong")

    def dang_nhap_that_bai(self):
        self.trinh_duyet.get("https://www.saucedemo.com/")
        self.dang_nhap("locked_out_user", "secret_sauce")
        loi = WebDriverWait(self.trinh_duyet, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message-container"))
        )
        assert loi.is_displayed()
        print("Dang nhap that bai")

    def them_san_pham_vao_gio(self):
        self.dang_nhap("standard_user", "secret_sauce")
        WebDriverWait(self.trinh_duyet, 10).until(
            EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        self.trinh_duyet.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        gio = self.trinh_duyet.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        assert gio == "1"
        print("Them san pham vao gio thanh cong")

    def xoa_san_pham_khoi_gio(self):
        self.them_san_pham_vao_gio()
        self.trinh_duyet.find_element(By.ID, "remove-sauce-labs-backpack").click()
        time.sleep(1)
        gio = self.trinh_duyet.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        assert len(gio) == 0
        print("Xoa san pham khoi gio thanh cong")

    def mua_hang_thanh_cong(self):
        self.them_san_pham_vao_gio()
        self.trinh_duyet.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(self.trinh_duyet, 5).until(
            EC.presence_of_element_located((By.ID, "checkout"))
        ).click()
        self.trinh_duyet.find_element(By.ID, "first-name").send_keys("Nguyen")
        self.trinh_duyet.find_element(By.ID, "last-name").send_keys("Quang")
        self.trinh_duyet.find_element(By.ID, "postal-code").send_keys("10000")
        self.trinh_duyet.find_element(By.ID, "continue").click()
        self.trinh_duyet.find_element(By.ID, "finish").click()
        thong_bao = WebDriverWait(self.trinh_duyet, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text
        assert "THANK YOU" in thong_bao.upper()
        print("Mua hang thanh cong")

    def dong_trinh_duyet(self):
        self.trinh_duyet.quit()


if __name__ == "__main__":
    kiem_thu = KiemThuSauceDemo()
    try:
        kiem_thu.dang_nhap_thanh_cong()
        kiem_thu.dang_nhap_that_bai()
        kiem_thu.them_san_pham_vao_gio()
        kiem_thu.xoa_san_pham_khoi_gio()
        kiem_thu.mua_hang_thanh_cong()
    finally:
        kiem_thu.dong_trinh_duyet()
