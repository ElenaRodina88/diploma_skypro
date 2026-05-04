import os
import allure
import requests
from dotenv import load_dotenv

load_dotenv(".env")

BASE_URL = os.getenv("GITHUB_API_BASE_URL", "https://api.github.com")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

@allure.step("API: Выполнить поиск репозиториев по запросу: {query}")
def make_search_request(query: str, token: str = None) -> requests.Response:
    """
    Выполняет поиск репозиториев GitHub по запросу.

    Входные данные:
        query (str): Запрос (например, 'test' или 'language:python').
        token (str | None): Токен GitHub для аутентификации.

    Выходные данные:
        requests.Response: Ответ от GitHub API.
    """
    url = f"{BASE_URL}/search/repositories"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    return requests.get(url, params={"q": query}, headers=headers)

@allure.step("API: Создать репозиторий с именем: {name}")
def create_repo(token: str, name: str, **data) -> requests.Response:
    """
    Создаёт новый репозиторий.

    Входные данные:
        token (str): Токен GitHub.
        name (str): Имя нового репозитория.
        **data: Дополнительные параметры для тела запроса.

    Выходные данные:
        requests.Response: Ответ от API.
    """
    url = f"{BASE_URL}/user/repos"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}",
    }
    payload = {"name": name, **data}
    return requests.post(url, json=payload, headers=headers)

@allure.step("API: Удалить репозиторий {owner}/{repo}")
def delete_repo(token: str, owner: str, repo: str) -> requests.Response:
    """
    Удаляет репозиторий для очистки тестового окружения.

    Входные данные:
        token (str): Токен GitHub
        owner (str): Владелец репозитория.
        repo (str): Имя репозитория.

    Выходные данные:
        requests.Response: Ответ от API.
    """
    url = f"{BASE_URL}/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}",
    }
    return requests.delete(url, headers=headers)
