import allure
import pytest
from pages.github_main_page import GitHubMainPage


@pytest.mark.ui
@allure.feature("GitHub UI")
@allure.story("Наличие поиска в хедере")
@allure.title("Отображение строки поиска в хедере платформы")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_is_present_in_header(driver, github_base_url):
    with allure.step("Открываем главную страницу GitHub"):
        driver.get(github_base_url)
        page = GitHubMainPage(driver)

    with allure.step("Проверяем наличие кнопки поиска"):
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
    with allure.step("Открываем главную страницу и выполняем поиск"):
        driver.get(github_base_url)
        page = GitHubMainPage(driver)
        page.perform_search("test")

    with allure.step("Проверяем наличие результатов поиска"):
        count = page.get_search_results_count()
        assert count > 0, f"Количество результатов должно быть больше 0, получено: {count}"


@pytest.mark.ui
@allure.feature("GitHub UI")
@allure.story("Навигация по результатам поиска")
@allure.title("Переход в репозиторий после его поиска")
@allure.severity(allure.severity_level.CRITICAL)
def test_click_first_repository_and_verify(driver, github_base_url):
    with allure.step("Выполняем поиск и переходим в первый репозиторий"):
        driver.get(github_base_url)
        page = GitHubMainPage(driver)
        page.perform_search("test")
        repo_name_from_search = page.click_first_repository()

    with allure.step("Проверяем соответствие URL и заголовка"):
        current_url = driver.current_url
        repo_header = driver.find_element("css selector", "a.d-block.overflow-x-hidden").text
        expected_repo = repo_name_from_search.split("/")[-1]

        assert expected_repo in current_url, f"URL не содержит {expected_repo}"
        assert expected_repo in repo_header, f"Заголовок не содержит {expected_repo}"


@pytest.mark.ui
@allure.feature("GitHub UI")
@allure.story("Создание репозитория")
@allure.title("Корректное отображение формы создания")
@allure.severity(allure.severity_level.CRITICAL)
def test_new_repository_form_is_accessible(driver, github_base_url):
    with allure.step("Открываем главную страницу и форму создания репозитория"):
        driver.get(github_base_url)
        page = GitHubMainPage(driver)
        page.open_new_repository_form()

    with allure.step("Проверяем корректность URL страницы создания репозитория"):
        assert "github.com/new" in driver.current_url, "URL не соответствует странице создания репозитория"

    with allure.step("Проверяем заголовок формы создания репозитория"):
        header = page.get_new_repo_form_header()
        assert "Create a new repository" in header, f"Заголовок не найден, получено: '{header}'"


@pytest.mark.ui
@allure.feature("GitHub UI")
@allure.story("Поиск")
@allure.title("Отображение ошибки при поиске несуществующего репозитория")
@allure.severity(allure.severity_level.NORMAL)
def test_search_error_for_nonexistent_repo(driver, github_base_url):
    page = GitHubMainPage(driver)
    random_query = "xyz123random987654321"

    with allure.step(f"Выполняем поиск несуществующего репозитория '{random_query}'"):
        driver.get(github_base_url)
        page.perform_search(random_query)

    with allure.step("Проверяем отображение сообщения об отсутствии результатов"):
        error_text = page.get_no_results_error_text()
        assert "Your search did not match any repositories" in error_text
