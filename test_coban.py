# File: kiem_test.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
import time

class KiemThuSauceDemo:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://www.saucedemo.com/"
        self.tai_khoan = "standard_user"  # Có thể thử "locked_out_user" để kiểm tra alert
        self.mat_khau = "secret_sauce"

    def xu_ly_thong_bao(self):
        """Kiểm tra và xử lý thông báo (alert) nếu có"""
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print(f"Thông báo: {alert_text} - Đã nhấn OK")
        except (TimeoutException, NoAlertPresentException):
            pass  # Không có alert thì bỏ qua
        # Kiểm tra modal HTML (nếu có)
        try:
            modal = self.driver.find_element(By.CLASS_NAME, "error-message-container")
            if modal.is_displayed():
                print(f"Modal HTML: {modal.text}")
                # Nếu có nút đóng hoặc OK, nhấn vào
                try:
                    modal.find_element(By.CLASS_NAME, "error-button").click()
                    print("Đã đóng modal HTML")
                except NoSuchElementException:
                    pass
        except NoSuchElementException:
            pass

    def mo_trang(self):
        self.driver.get(self.url)
        self.xu_ly_thong_bao()

    def dang_nhap(self):
        try:
            self.xu_ly_thong_bao()  # Kiểm tra trước khi đăng nhập
            self.wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(self.tai_khoan)
            self.driver.find_element(By.ID, "password").send_keys(self.mat_khau)
            self.driver.find_element(By.ID, "login-button").click()
            self.xu_ly_thong_bao()  # Kiểm tra sau khi đăng nhập
            if "inventory" in self.driver.current_url:
                print("Dang nhap thanh cong")
            else:
                print("Dang nhap that bai")
        except Exception as e:
            print(f"Loi dang nhap: {str(e)}")

    def kiem_tra_danh_sach_san_pham(self):
        try:
            self.xu_ly_thong_bao()
            san_pham = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))
            print(f"Tim thay {len(san_pham)} san pham")
        except Exception as e:
            print(f"Loi kiem tra danh sach san pham: {str(e)}")

    def them_san_pham_vao_gio(self):
        try:
            self.xu_ly_thong_bao()
            them_buttons = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[id^='add-to-cart']")))
            them_buttons[0].click()
            self.xu_ly_thong_bao()
            them_buttons[1].click()
            self.xu_ly_thong_bao()
            try:
                gio_hang = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
                if gio_hang.text == "2":
                    print("Them 2 san pham vao gio hang thanh cong")
                else:
                    print(f"Them san pham vao gio hang, nhung so luong la {gio_hang.text}")
            except TimeoutException:
                print("Khong tim thay chi so gio hang")
        except Exception as e:
            print(f"Loi them san pham: {str(e)}")

    def xem_gio_hang(self):
        try:
            self.xu_ly_thong_bao()
            self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
            self.xu_ly_thong_bao()
            san_pham_trong_gio = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item")))
            if len(san_pham_trong_gio) == 2:
                print("Xem gio hang: Co 2 san pham")
            else:
                print(f"Xem gio hang: Co {len(san_pham_trong_gio)} san pham")
        except Exception as e:
            print(f"Loi xem gio hang: {str(e)}")

    def thanh_toan(self):
        try:
            self.xu_ly_thong_bao()
            self.driver.find_element(By.ID, "checkout").click()
            self.xu_ly_thong_bao()
            self.wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Nguyen")
            self.driver.find_element(By.ID, "last-name").send_keys("Van A")
            self.driver.find_element(By.ID, "postal-code").send_keys("12345")
            self.driver.find_element(By.ID, "continue").click()
            self.xu_ly_thong_bao()
            self.driver.find_element(By.ID, "finish").click()
            self.xu_ly_thong_bao()
            thong_bao = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
            if "Thank you for your order!" in thong_bao.text:
                print("Thanh toan thanh cong")
            else:
                print("Thanh toan that bai")
        except Exception as e:
            print(f"Loi thanh toan: {str(e)}")

    def dang_xuat(self):
        try:
            self.xu_ly_thong_bao()
            self.driver.find_element(By.ID, "react-burger-menu-btn").click()
            self.wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()
            self.xu_ly_thong_bao()
            if "saucedemo.com" in self.driver.current_url:
                print("Dang xuat thanh cong")
            else:
                print("Dang xuat that bai")
        except Exception as e:
            print(f"Loi dang xuat: {str(e)}")

    def chay_kiem_thu(self):
        try:
            self.mo_trang()
            self.dang_nhap()
            self.kiem_tra_danh_sach_san_pham()
            self.them_san_pham_vao_gio()
            self.xem_gio_hang()
            self.thanh_toan()
            self.dang_xuat()
        except Exception as e:
            print(f"Loi tong the: {str(e)}")
        finally:
            time.sleep(2)
            self.driver.quit()

if __name__ == "__main__":
    kiem_thu = KiemThuSauceDemo()
    kiem_thu.chay_kiem_thu()