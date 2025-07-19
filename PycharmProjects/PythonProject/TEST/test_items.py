from selenium.webdriver.common.by import By
import time

def test_add_to_cart_button_present(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
    browser.get(link)
    time.sleep(2)  # чтобы визуально увидеть язык страницы (по заданию)
    add_to_cart_btn = browser.find_element(By.CSS_SELECTOR, ".btn-add-to-basket")
    assert add_to_cart_btn, "Кнопка 'Добавить в корзину' не найдена"
