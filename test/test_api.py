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
    response = make_search_request("test", token=GITHUB_TOKEN)
    assert_ok_response(response)


@pytest.mark.api
@allure.feature("GitHub API")
@allure.story("Поиск репозиториев")
@allure.title("Поиск репозитория по языку программирования")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_repositories_by_language_python():
    response = make_search_request("language:python", token=GITHUB_TOKEN)
    assert_ok_response(response)


@pytest.mark.api
@allure.feature("GitHub API")
@allure.story("Валидация запросов")
@allure.title("Поиск репозитория с количеством операторов OR/AND/NOT больше пяти в запросе ")
@allure.severity(allure.severity_level.NORMAL)
def test_search_repositories_too_many_operators():
    query = "testing AND python OR api AND javascript OR ruby NOT php AND java"
    response = make_search_request(query, token=GITHUB_TOKEN)

    assert 400 <= response.status_code < 500
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
    response = create_repo(token=GITHUB_TOKEN, name=repo_name)
    assert_ok_response(response)
    PUBLIC_REPO_NAME = response.json()["name"]


@pytest.mark.api
@allure.feature("GitHub API")
@allure.story("Управление репозиториями")
@allure.title("Невозможность создания репозитория с уже существующим названием")
@allure.severity(allure.severity_level.NORMAL)
def test_cannot_create_repo_with_existing_name():
    response = create_repo(token=GITHUB_TOKEN, name=PUBLIC_REPO_NAME)
    assert 400 <= response.status_code < 500
    assert response.json()["errors"][0]["message"] == "name already exists on this account"


@pytest.mark.api
@allure.feature("GitHub API")
@allure.story("Управление репозиториями")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_public_repo():
    owner = os.getenv("GITHUB_OWNER", "")
    response = delete_repo(token=GITHUB_TOKEN, owner=owner, repo=PUBLIC_REPO_NAME)
    assert_ok_response(response)
