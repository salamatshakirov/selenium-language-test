import time
import math
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

answer = str(math.log(int(time.time())))

# Добавь сюда свои данные — НИКОГДА НЕ ПУБЛИКУЙ ИХ
EMAIL = "salamatshakirov96@gmail.com"
PASSWORD = "qwerty24566"

links = [
    "https://stepik.org/lesson/236895/step/1",
    "https://stepik.org/lesson/236896/step/1",
    "https://stepik.org/lesson/236897/step/1",
    "https://stepik.org/lesson/236898/step/1",
    "https://stepik.org/lesson/236899/step/1",
    "https://stepik.org/lesson/236903/step/1",
    "https://stepik.org/lesson/236904/step/1",
    "https://stepik.org/lesson/236905/step/1"
]


@pytest.fixture(scope="function")
def browser():
    print("\nЗапускаю браузер...")
    browser = webdriver.Chrome()
    yield browser
    print("Закрываю браузер...")
    browser.quit()


@pytest.mark.parametrize('link', links)
def test_stepik_login_and_submit(browser, link):
    browser.implicitly_wait(5)
    browser.get(link)

    # Нажимаем "Войти"
    login_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.navbar__auth_login"))
    )
    login_btn.click()

    # Вводим логин и пароль
    email_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "login"))
    )
    password_input = browser.find_element(By.NAME, "password")

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    # Ждем, когда окно логина исчезнет
    WebDriverWait(browser, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".sign-form"))
    )

    # Ждем загрузку поля для ответа
    textarea = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea"))
    )

    # Очищаем поле и вводим ответ
    answer = str(math.log(int(time.time())))
    textarea.clear()
    textarea.send_keys(answer)

    browser.execute_script(
        "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", textarea
    )

    # Нажимаем кнопку "Отправить"
    submit_btn = browser.find_element(By.CSS_SELECTOR, "button.submit-submission")
    submit_btn.click()

    # Проверяем фидбек "Correct!"
    feedback = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".smart-hints__hint"))
    )
    assert feedback.text == "Correct!", f"Ожидалось 'Correct!', но было '{feedback.text}'"
