import pytest
import allure
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.github_login_page import GitHubLoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(".env")


@pytest.fixture(scope="session")
def driver():
    """
    Инициализация драйвера.
    """
    with allure.step("Инициализация браузера Chrome"):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        yield driver
        with allure.step("Закрытие браузера"):
            driver.quit()


@pytest.fixture(scope="session", autouse=True)
def setup_authenticated_session(driver, github_base_url, user_login, user_password):
    """
    Выполняет авторизацию перед запуском тестов.
    """
    with allure.step(f"Авторизация пользователя: {user_login}"):
        login_page = GitHubLoginPage(driver)

        with allure.step("Переход на страницу логина"):
            login_page.open(github_base_url)

        with allure.step("Ввод учетных данных и отправка формы"):
            login_page.fill_credentials(user_login, user_password)
            login_page.submit()

        with allure.step("Ожидание успешной авторизации"):
            WebDriverWait(driver, 15).until_not(EC.url_contains("/login"))


@pytest.fixture(scope="session")
def github_base_url():
    return os.getenv("GITHUB_BASE_URL", "https://github.com")


@pytest.fixture(scope="session")
def user_login():
    return os.getenv("USER_LOGIN")


@pytest.fixture(scope="session")
def user_password():
    return os.getenv("USER_PASSWORD")
