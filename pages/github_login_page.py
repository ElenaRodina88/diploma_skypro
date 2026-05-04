import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GitHubLoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть страницу авторизации")
    def open(self, base_url: str) -> None:
        """
        Переходит на страницу логина GitHub.
        """
        self.driver.get(f"{base_url}/login")

    @property
    def login_input(self):
        return self.wait.until(EC.visibility_of_element_located((By.ID, "login_field")))

    @property
    def password_input(self):
        return self.wait.until(EC.visibility_of_element_located((By.ID, "password")))

    @allure.step("Заполнить данные пользователя: {username}")
    def fill_credentials(self, username: str, password: str) -> None:
        """
        Вводит логин и пароль в соответствующие поля.
        """
        self.login_input.send_keys(username)
        self.password_input.send_keys(password)

    @allure.step("Подтвердить вход (кнопка 'Sign in')")
    def submit(self) -> None:
        """
        Нажимает кнопку подтверждения входа
        """
        self.wait.until(EC.element_to_be_clickable((By.NAME, "commit"))).click()

    @allure.step("Создать репозиторий: {repo_name}")
    def create_repository(self, repo_name: str) -> None:
        """
        Заполняет форму создания репозитория и сохраняет его.
        """
        repo_input = self.wait.until(EC.visibility_of_element_located((By.ID, "repository-name-input")))
        repo_input.clear()
        repo_input.send_keys(repo_name)

        create_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create repository')]")))
        create_btn.click()
