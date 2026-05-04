import os
import pytest
import allure
import requests
from dotenv import load_dotenv
from objects.github_api import (
    GITHUB_TOKEN,
    make_search_request,
    create_repo,
    delete_repo,
)

load_dotenv(".env")

MAX_RESPONSE_TIME_MS = 3000
PUBLIC_REPO_NAME = None


def assert_ok_response(response: requests.Response):
    """
    Проверяет, что статус ответа 200–299 и время ответа < 3000 мс.
    """
    assert 200 <= response.status_code < 300, f"Expected 200–299, got {response.status_code}"
    response_time_ms = response.elapsed.total_seconds() * 1000
    assert response_time_ms < MAX_RESPONSE_TIME_MS, f"Response time {response_time_ms} ms"


@pytest.mark.api
@allure.feature("GitHub API")
@allure.story("Поиск репозиториев")
@allure.title("Поиск репозитория по запросу")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_repositories_by_query():
    with allure.step("Выполняем поиск репозиториев по запросу 'test'"):
        response = make_search_request("test", token=GITHUB_TOKEN)

    with allure.step("Проверяем успешный ответ API"):
        assert_ok_response(response)


@pytest.mark.api
@allure.feature("GitHub API")
@allure.story("Поиск репозиториев")
@allure.title("Поиск репозитория по языку программирования")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_repositories_by_language_python():
    with allure.step("Выполняем поиск репозиториев на языке программирования Python"):
        response = make_search_request("language:python", token=GITHUB_TOKEN)

    with allure.step("Проверяем успешный ответ API"):
        assert_ok_response(response)


@pytest.mark.api
@allure.feature("GitHub API")
@allure.story("Валидация запросов")
@allure.title("Поиск репозитория с количеством операторов OR/AND/NOT больше пяти в запросе ")
@allure.severity(allure.severity_level.NORMAL)
def test_search_repositories_too_many_operators():
    query = "testing AND python OR api AND javascript OR ruby NOT php AND java"

    with allure.step(f"Выполняем поиск с запросом содержащим >5 операторов: '{query}'"):
        response = make_search_request(query, token=GITHUB_TOKEN)

    with allure.step("Проверяем статус 4xx"):
        assert 400 <= response.status_code < 500

    with allure.step("Проверяем текст ошибки API"):
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["message"] == "More than five AND / OR / NOT operators were used."


@pytest.mark.api
@allure.feature("GitHub API")
@allure.story("Управление репозиториями")
@allure.title("Создание публичного репозитория")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_public_repo():
    global PUBLIC_REPO_NAME
    repo_name = "test_public"
    owner = os.getenv("GITHUB_OWNER", "")

    with allure.step(f"Создаём публичный репозиторий '{repo_name}'"):
        response = create_repo(token=GITHUB_TOKEN, name=repo_name)

    with allure.step("Проверяем успешное создание репозитория"):
        assert_ok_response(response)
        PUBLIC_REPO_NAME = response.json()["name"]

    with allure.step(f"Очищаем тестовую среду - удаляем репозиторий '{repo_name}'"):
        delete_response = delete_repo(token=GITHUB_TOKEN, owner=owner, repo=PUBLIC_REPO_NAME)
        assert_ok_response(delete_response)


@pytest.mark.api
@allure.feature("GitHub API")
@allure.story("Управление репозиториями")
@allure.title("Невозможность создания репозитория с уже существующим названием")
@allure.severity(allure.severity_level.NORMAL)
def test_cannot_create_repo_with_existing_name():
    global PUBLIC_REPO_NAME
    repo_name = "test_duplicate_repository"
    owner = os.getenv("GITHUB_OWNER", "")

    with allure.step(f"Создаём репозиторий '{repo_name}' для проверки дублирования"):
        create_response = create_repo(token=GITHUB_TOKEN, name=repo_name)
        assert_ok_response(create_response)
        PUBLIC_REPO_NAME = create_response.json()["name"]

    with allure.step(f"Пытаемся создать репозиторий с уже существующим именем '{PUBLIC_REPO_NAME}'"):
        duplicate_response = create_repo(token=GITHUB_TOKEN, name=PUBLIC_REPO_NAME)

    with allure.step("Проверяем статус 4xx"):
        assert 400 <= duplicate_response.status_code < 500

    with allure.step("Проверяем сообщение об ошибке"):
        assert duplicate_response.json()["errors"][0]["message"] == "name already exists on this account"

    with allure.step(f"Очищаем тестовую среду - удаляем репозиторий '{PUBLIC_REPO_NAME}'"):
        delete_response = delete_repo(token=GITHUB_TOKEN, owner=owner, repo=PUBLIC_REPO_NAME)
        assert_ok_response(delete_response)
