import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.github_main_page import GitHubMainPage


@pytest.mark.ui
@allure.feature("GitHub UI")
@allure.story("Наличие поиска в хедере")
@allure.title("Отображение строки поиска в хедере платформы")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_is_present_in_header(driver, github_base_url):
    driver.get(github_base_url)
    page = GitHubMainPage(driver)

    if not page.is_search_button_present():
        allure.attach(driver.get_screenshot_as_png(), name="search_button_missing",
                      attachment_type=allure.attachment_type.PNG)

    assert page.is_search_button_present(), f"Кнопка поиска не найдена на {driver.current_url}"


@pytest.mark.ui
@allure.feature("GitHub UI")
@allure.story("Поиск репозиториев")
@allure.title("Поиск репозиториев по ключевому слову")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_results_count_is_not_zero(driver, github_base_url):
    driver.get(github_base_url)
    page = GitHubMainPage(driver)

    page.perform_search("test")

    WebDriverWait(driver, 10).until(lambda d: "search" in d.current_url)
    count = page.get_search_results_count()

    assert count > 0, f"Количество результатов должно быть больше 0, получено: {count}"


@pytest.mark.ui
@allure.feature("GitHub UI")
@allure.story("Навигация по результатам поиска")
@allure.title("Переход в репозиторий после его поиска")
@allure.severity(allure.severity_level.CRITICAL)
def test_click_first_repository_and_verify(driver, github_base_url):
    driver.get(github_base_url)
    page = GitHubMainPage(driver)

    page.perform_search("test")
    repo_name_from_search = page.click_first_repository()

    with allure.step("Проверка соответствия URL и заголовка"):
        current_url = driver.current_url
        repo_header = driver.find_element(By.CSS_SELECTOR, "a.d-block.overflow-x-hidden").text
        expected_repo = repo_name_from_search.split("/")[-1]

        assert expected_repo in current_url, f"URL не содержит {expected_repo}"
        assert expected_repo in repo_header, f"Заголовок не содержит {expected_repo}"


@pytest.mark.ui
@allure.feature("GitHub UI")
@allure.story("Создание репозитория")
@allure.title("Корректное отображение формы создания")
@allure.severity(allure.severity_level.CRITICAL)
def test_new_repository_form_is_accessible(driver, github_base_url):
    driver.get(github_base_url)
    page = GitHubMainPage(driver)

    page.open_new_repository_form()

    assert "github.com/new" in driver.current_url, "URL не соответствует странице создания"

    header_locator = (By.CSS_SELECTOR, "h1.prc-Heading-Heading-MtWFE")
    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(header_locator)
    ).text.strip()

    assert "Create a new repository" in header, f"Заголовок не найден, получено: '{header}'"


@pytest.mark.ui
@allure.feature("GitHub UI")
@allure.story("Поиск")
@allure.title("Отображение ошибки при поиске несуществующего репозитория")
@allure.severity(allure.severity_level.NORMAL)
def test_search_error_for_nonexistent_repo(driver, github_base_url):
    page = GitHubMainPage(driver)
    random_query = "xyz123random987654321"

    driver.get(github_base_url)
    page.perform_search(random_query)

    WebDriverWait(driver, 10).until(EC.url_contains("/search"))
    error_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3.Header-module__heading__i_Q19"))
    )

    assert "Your search did not match any repositories" in error_element.text.strip()
