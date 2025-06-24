import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class KiemThuSauceDemo(unittest.TestCase):
    
    def setUp(self):
        """Khởi tạo trình duyệt trước mỗi test"""
        # Sử dụng webdriver-manager để tự động tải và cấu hình ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()  # Phóng to cửa sổ trình duyệt
        self.wait = WebDriverWait(self.driver, 10)  # Thiết lập thời gian chờ tối đa 10 giây
        self.base_url = "https://www.saucedemo.com"  # URL cơ bản của trang web
        
    def tearDown(self):
        """Đóng trình duyệt sau mỗi test"""
        self.driver.quit()
        
    def dang_nhap(self, username="standard_user", password="secret_sauce"):
        """Hàm hỗ trợ đăng nhập"""
        self.driver.get(self.base_url)  # Mở trang web
        # Chờ trường tên người dùng xuất hiện và nhập thông tin
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        
        username_field.clear()  # Xóa nội dung trường tên người dùng
        username_field.send_keys(username)  # Nhập tên người dùng
        password_field.clear()  # Xóa nội dung trường mật khẩu
        password_field.send_keys(password)  # Nhập mật khẩu
        login_button.click()  # Nhấn nút đăng nhập
        
    def test_01_kiem_tra_trang_chu(self):
        """Kiểm tra tải trang chủ thành công"""
        self.driver.get(self.base_url)  # Mở trang chủ
        
        # Kiểm tra tiêu đề trang có chứa "Swag Labs"
        self.assertIn("Swag Labs", self.driver.title)
        
        # Kiểm tra sự tồn tại của các thành phần giao diện trên trang chủ
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "login_logo"))
        self.assertTrue(self.driver.find_element(By.ID, "user-name"))
        self.assertTrue(self.driver.find_element(By.ID, "password"))
        self.assertTrue(self.driver.find_element(By.ID, "login-button"))
        
    def test_02_dang_nhap_thanh_cong(self):
        """Kiểm tra đăng nhập thành công với tài khoản hợp lệ"""
        self.dang_nhap()  # Gọi hàm đăng nhập với thông tin mặc định
        
        # Chờ URL chứa "/inventory.html" để xác nhận chuyển hướng thành công
        self.wait.until(EC.url_contains("/inventory.html"))
        self.assertIn("/inventory.html", self.driver.current_url)
        
        # Kiểm tra logo "Swag Labs" hiển thị trên trang sản phẩm
        header = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "app_logo")))
        self.assertEqual(header.text, "Swag Labs")
        
    def test_03_dang_nhap_that_bai_sai_mat_khau(self):
        """Kiểm tra đăng nhập thất bại khi nhập sai mật khẩu"""
        self.driver.get(self.base_url)  # Mở trang chủ
        
        # Nhập thông tin đăng nhập với mật khẩu sai
        username_field = self.driver.find_element(By.ID, "user-name")
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("sai_mat_khau")
        login_button.click()
        
        # Kiểm tra thông báo lỗi
        error_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        self.assertIn("Username and password do not match", error_message.text)
        
    def test_04_dang_nhap_tai_khoan_bi_khoa(self):
        """Kiểm tra đăng nhập với tài khoản bị khóa"""
        self.dang_nhap("locked_out_user", "secret_sauce")  # Đăng nhập với tài khoản bị khóa
        
        # Kiểm tra thông báo lỗi
        error_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        self.assertIn("locked out", error_message.text)
        
    def test_05_hien_thi_danh_sach_san_pham(self):
        """Kiểm tra hiển thị danh sách sản phẩm"""
        self.dang_nhap()  # Đăng nhập
        
        # Kiểm tra có sản phẩm hiển thị
        products = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))
        self.assertGreater(len(products), 0)  # Đảm bảo có ít nhất 1 sản phẩm
        
        # Kiểm tra thông tin sản phẩm đầu tiên
        first_product = products[0]
        product_name = first_product.find_element(By.CLASS_NAME, "inventory_item_name")
        product_price = first_product.find_element(By.CLASS_NAME, "inventory_item_price")
        
        self.assertTrue(product_name.text)  # Tên sản phẩm không rỗng
        self.assertTrue(product_price.text)  # Giá sản phẩm không rỗng
        self.assertIn("$", product_price.text)  # Giá có ký hiệu đô la
        
    def test_06_sap_xep_san_pham(self):
        """Kiểm tra chức năng sắp xếp sản phẩm"""
        self.dang_nhap()  # Đăng nhập
        
        # Sắp xếp theo tên A-Z
        sort_dropdown = Select(self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))))
        sort_dropdown.select_by_value("az")
        
        time.sleep(1)  # Chờ giao diện cập nhật
        product_names = [elem.text for elem in self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        self.assertEqual(product_names, sorted(product_names))  # Kiểm tra danh sách tên đã được sắp xếp
        
        # Sắp xếp theo giá thấp đến cao
        sort_dropdown.select_by_value("lohi")
        time.sleep(1)  # Chờ giao diện cập nhật
        
        prices = []
        for price_elem in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price"):
            price_text = price_elem.text.replace("$", "")
            prices.append(float(price_text))
        
        self.assertEqual(prices, sorted(prices))  # Kiểm tra danh sách giá đã được sắp xếp
        
    def test_07_them_san_pham_vao_gio_hang(self):
        """Kiểm tra thêm sản phẩm vào giỏ hàng"""
        self.dang_nhap()  # Đăng nhập
        
        # Lấy số lượng sản phẩm trong giỏ hàng ban đầu
        try:
            cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            initial_count = int(cart_badge.text)
        except NoSuchElementException:
            initial_count = 0  # Giỏ hàng rỗng
            
        # Thêm sản phẩm đầu tiên vào giỏ hàng
        add_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test^='add-to-cart']")))
        add_button.click()
        
        # Kiểm tra số lượng trong giỏ hàng tăng lên
        cart_badge = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        new_count = int(cart_badge.text)
        self.assertEqual(new_count, initial_count + 1)
        
        # Kiểm tra nút chuyển thành "Remove"
        remove_button = self.driver.find_element(By.CSS_SELECTOR, "[data-test^='remove']")
        self.assertTrue(remove_button.is_displayed())
        
    def test_08_xoa_san_pham_khoi_gio_hang(self):
        """Kiểm tra xóa sản phẩm khỏi giỏ hàng"""
        self.dang_nhap()  # Đăng nhập
        
        # Thêm sản phẩm vào giỏ hàng
        add_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test^='add-to-cart']")))
        add_button.click()
        
        # Xóa sản phẩm
        remove_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test^='remove']")))
        remove_button.click()
        
        # Kiểm tra nút chuyển về "Add to cart"
        add_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test^='add-to-cart']")))
        self.assertTrue(add_button.is_displayed())
        
        # Kiểm tra badge giỏ hàng biến mất hoặc bằng 0
        try:
            cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            self.assertEqual(cart_badge.text, "0")
        except NoSuchElementException:
            pass  # Badge biến mất là đúng
            
    def test_09_xem_chi_tiet_san_pham(self):
        """Kiểm tra xem chi tiết sản phẩm"""
        self.dang_nhap()  # Đăng nhập
        
        # Click vào tên sản phẩm đầu tiên
        product_name = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "inventory_item_name")))
        product_name_text = product_name.text
        product_name.click()
        
        # Kiểm tra chuyển đến trang chi tiết
        self.wait.until(EC.url_contains("/inventory-item.html"))
        
        # Kiểm tra thông tin chi tiết sản phẩm
        detail_name = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_details_name")))
        self.assertEqual(detail_name.text, product_name_text)
        
        # Kiểm tra các thành phần: hình ảnh, mô tả, giá
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "inventory_details_img"))
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "inventory_details_desc"))
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "inventory_details_price"))
        
        # Kiểm tra nút "Back to products"
        back_button = self.driver.find_element(By.ID, "back-to-products")
        self.assertTrue(back_button.is_displayed())
        
    def test_10_quay_lai_danh_sach_san_pham(self):
        """Kiểm tra quay lại danh sách sản phẩm từ trang chi tiết"""
        self.dang_nhap()  # Đăng nhập
        
        # Vào trang chi tiết sản phẩm
        product_name = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "inventory_item_name")))
        product_name.click()
        
        # Nhấn nút quay lại
        back_button = self.wait.until(EC.element_to_be_clickable((By.ID, "back-to-products")))
        back_button.click()
        
        # Kiểm tra quay về trang danh sách sản phẩm
        self.wait.until(EC.url_contains("/inventory.html"))
        self.assertIn("/inventory.html", self.driver.current_url)
        
    def test_11_xem_gio_hang(self):
        """Kiểm tra xem giỏ hàng"""
        self.dang_nhap()  # Đăng nhập
        
        # Thêm 2 sản phẩm vào giỏ hàng
        add_buttons = self.driver.find_elements(By.CSS_SELECTOR, "[data-test^='add-to-cart']")[:2]
        for button in add_buttons:
            button.click()
            time.sleep(0.5)  # Chờ giao diện cập nhật
            
        # Vào giỏ hàng
        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
        
        # Kiểm tra trang giỏ hàng
        self.wait.until(EC.url_contains("/cart.html"))
        
        # Kiểm tra có 2 sản phẩm trong giỏ
        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(cart_items), 2)
        
        # Kiểm tra các nút trong giỏ hàng
        self.assertTrue(self.driver.find_element(By.ID, "continue-shopping"))
        self.assertTrue(self.driver.find_element(By.ID, "checkout"))
        
    def test_12_tiep_tuc_mua_hang(self):
        """Kiểm tra tiếp tục mua hàng từ giỏ hàng"""
        self.dang_nhap()  # Đăng nhập
        
        # Vào giỏ hàng
        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
        
        # Nhấn nút "Continue Shopping"
        continue_button = self.wait.until(EC.element_to_be_clickable((By.ID, "continue-shopping")))
        continue_button.click()
        
        # Kiểm tra quay về trang danh sách sản phẩm
        self.wait.until(EC.url_contains("/inventory.html"))
        
    def test_13_thanh_toan_thong_tin_hop_le(self):
        """Kiểm tra thanh toán với thông tin hợp lệ"""
        self.dang_nhap()  # Đăng nhập
        
        # Thêm sản phẩm vào giỏ hàng
        add_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test^='add-to-cart']")))
        add_button.click()
        
        # Vào giỏ hàng và nhấn checkout
        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
        
        checkout_button = self.wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
        checkout_button.click()
        
        # Nhập thông tin thanh toán
        first_name = self.wait.until(EC.presence_of_element_located((By.ID, "first-name")))
        last_name = self.driver.find_element(By.ID, "last-name")
        postal_code = self.driver.find_element(By.ID, "postal-code")
        
        first_name.send_keys("Nguyen")
        last_name.send_keys("Van A")
        postal_code.send_keys("10000")
        
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        
        # Kiểm tra chuyển đến trang xác nhận đơn hàng
        self.wait.until(EC.url_contains("/checkout-step-two.html"))
        
        # Kiểm tra thông tin đơn hàng
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "cart_item"))
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "summary_total_label"))
        
    def test_14_thanh_toan_thieu_thong_tin(self):
        """Kiểm tra thanh toán khi thiếu thông tin"""
        self.dang_nhap()  # Đăng nhập
        
        # Thêm sản phẩm vào giỏ hàng
        add_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test^='add-to-cart']")))
        add_button.click()
        
        # Vào giỏ hàng và nhấn checkout
        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
        
        checkout_button = self.wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
        checkout_button.click()
        
        # Nhấn nút continue mà không nhập thông tin
        continue_button = self.wait.until(EC.element_to_be_clickable((By.ID, "continue")))
        continue_button.click()
        
        # Kiểm tra thông báo lỗi
        error_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        self.assertIn("First Name is required", error_message.text)
        
    def test_15_hoan_thanh_don_hang(self):
        """Kiểm tra hoàn thành đơn hàng"""
        self.dang_nhap()  # Đăng nhập
        
        # Thêm sản phẩm, vào giỏ hàng, nhấn checkout
        add_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test^='add-to-cart']")))
        add_button.click()
        
        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
        
        checkout_button = self.wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
        checkout_button.click()
        
        # Nhập thông tin thanh toán
        first_name = self.wait.until(EC.presence_of_element_located((By.ID, "first-name")))
        last_name = self.driver.find_element(By.ID, "last-name")
        postal_code = self.driver.find_element(By.ID, "postal-code")
        
        first_name.send_keys("Nguyen")
        last_name.send_keys("Van A")
        postal_code.send_keys("10000")
        
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        
        # Nhấn nút hoàn thành đơn hàng
        finish_button = self.wait.until(EC.element_to_be_clickable((By.ID, "finish")))
        finish_button.click()  # Sửa từ finish_string thành finish_button
        
        # Kiểm tra trang hoàn thành đơn hàng
        self.wait.until(EC.url_contains("/checkout-complete.html"))
        
        # Kiểm tra thông báo thành công
        success_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
        self.assertIn("Thank you for your order", success_message.text)
        
        # Kiểm tra nút "Back Home"
        back_home_button = self.driver.find_element(By.ID, "back-to-products")
        self.assertTrue(back_home_button.is_displayed())
        
    def test_16_menu_ham_burger(self):
        """Kiểm tra menu hamburger"""
        self.dang_nhap()  # Đăng nhập
        
        # Mở menu hamburger
        menu_button = self.wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
        menu_button.click()
        
        # Kiểm tra các mục trong menu
        self.wait.until(EC.element_to_be_clickable((By.ID, "inventory_sidebar_link")))
        self.assertTrue(self.driver.find_element(By.ID, "inventory_sidebar_link"))
        self.assertTrue(self.driver.find_element(By.ID, "about_sidebar_link"))
        self.assertTrue(self.driver.find_element(By.ID, "logout_sidebar_link"))
        self.assertTrue(self.driver.find_element(By.ID, "reset_sidebar_link"))
        
    def test_17_dang_xuat(self):
        """Kiểm tra đăng xuất"""
        self.dang_nhap()  # Đăng nhập
        
        # Mở menu và đăng xuất
        menu_button = self.wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
        menu_button.click()
        
        logout_button = self.wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
        logout_button.click()
        
        # Kiểm tra quay về trang đăng nhập
        self.wait.until(EC.url_to_be(self.base_url + "/"))
        self.assertEqual(self.driver.current_url, self.base_url + "/")
        
        # Kiểm tra các trường đăng nhập hiển thị
        self.assertTrue(self.driver.find_element(By.ID, "user-name"))
        self.assertTrue(self.driver.find_element(By.ID, "password"))
        
    def test_18_reset_app_state(self):
        """Kiểm tra reset trạng thái ứng dụng"""
        self.dang_nhap()  # Đăng nhập
        
        # Thêm sản phẩm vào giỏ hàng
        add_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test^='add-to-cart']")))
        add_button.click()
        
        # Kiểm tra badge giỏ hàng hiển thị
        cart_badge = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        self.assertEqual(cart_badge.text, "1")
        
        # Mở menu và reset trạng thái
        menu_button = self.driver.find_element(By.ID, "react-burger-menu-btn")
        menu_button.click()
        
        reset_button = self.wait.until(EC.element_to_be_clickable((By.ID, "reset_sidebar_link")))
        reset_button.click()
        
        # Đóng menu
        close_button = self.driver.find_element(By.ID, "react-burger-cross-btn")
        close_button.click()
        
        # Kiểm tra giỏ hàng đã được reset
        time.sleep(1)  # Chờ reset hoàn thành
        try:
            cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            self.fail("Badge giỏ hàng vẫn còn sau khi reset")
        except NoSuchElementException:
            pass  # Badge biến mất là đúng
            
    def test_19_tai_khoan_problem_user(self):
        """Kiểm tra tài khoản problem_user"""
        self.dang_nhap("problem_user", "secret_sauce")  # Đăng nhập với tài khoản có vấn đề
        
        # Kiểm tra đăng nhập thành công
        self.wait.until(EC.url_contains("/inventory.html"))
        
        # Kiểm tra danh sách sản phẩm hiển thị (có thể có lỗi giao diện)
        products = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))
        self.assertGreater(len(products), 0)
        
    def test_20_tai_khoan_performance_glitch_user(self):
        """Kiểm tra tài khoản performance_glitch_user"""
        self.dang_nhap("performance_glitch_user", "secret_sauce")  # Đăng nhập với tài khoản chậm
        
        # Kiểm tra đăng nhập thành công (có thể chậm)
        self.wait.until(EC.url_contains("/inventory.html"))
        
        # Kiểm tra danh sách sản phẩm hiển thị
        products = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))
        self.assertGreater(len(products), 0)

if __name__ == "__main__":
    # Chạy tất cả các test
    unittest.main(verbosity=2)