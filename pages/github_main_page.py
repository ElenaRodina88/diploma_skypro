import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GitHubMainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Проверить наличие кнопки поиска в хедере")
    def is_search_button_present(self) -> bool:
        """
        Проверяет видимость кнопки поиска.
        """
        try:
            button = self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "button[aria-label='Search or jump to…']")
                )
            )
            return button.is_displayed()
        except Exception:
            return False

    @allure.step("Выполнить поиск: {query}")
    def perform_search(self, query: str) -> None:
        """
        Вводит текст запроса в поиск и нажимает Enter.

        Входные данные:
            query (str): Текст поискового запроса.
        """
        search_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Search or jump to…']"))
        )
        search_btn.click()

        search_input = self.wait.until(EC.visibility_of_element_located((By.ID, "query-builder-test")))
        search_input.send_keys(query + Keys.ENTER)

        self.wait.until(EC.url_contains("/search"))

    @allure.step("Получить количество результатов поиска")
    def get_search_results_count(self) -> int:
        """
        Получает количество найденных репозиториев.

        Выходные данные:
            int: Число найденных элементов.
        """
        count_text = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "SearchSubHeader-module__inlineDisplay__AFA2a"))
        ).text
        number_part = count_text.split(" ")[0].replace("M", "000000").replace("k", "000")
        return int(number_part)

    @allure.step("Кликнуть по первому репозиторию в результатах")
    def click_first_repository(self) -> str:
        """
        Нажимает на первую ссылку репозитория.

        Выходные данные:
            str: Название репозитория, по которому был клик.
        """
        first_repo_link = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[data-testid='results-list'] a.prc-Link-Link-9ZwDx")
            )
        )
        repo_name = first_repo_link.text
        first_repo_link.click()
        return repo_name


    @allure.step("Открыть форму создания нового репозитория")
    def open_new_repository_form(self) -> None:
        """
        Открывает меню создания и переходит на страницу 'New repository'.
        """
        menu_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-haspopup='true'].GlobalCreateMenu-module__actionMenuButton__Hj_iB")
            )
        )
        menu_button.click()

        new_repo_item = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'New repository')]"))
        )
        new_repo_item.click()

        self.wait.until(EC.url_contains("/new"))
