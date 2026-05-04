# Автоматизированное тестирование GitHub (API/UI) 

Проект автоматизированного тестирования платформы GitHub. Включает в себя API-тесты и UI-тесты с поддержкой генерации отчетов в `Allure`.

## Описание проекта
Цель проекта — обеспечить автоматизированную проверку функционала GitHub:
- **API**: Поиск репозиториев, управление (создание/удаление) репозиториями, обработка ошибок API.
- **UI**: Проверка хедера, навигация по поиску, тестирование формы создания репозитория.

## Структура проекта
```text
Diploma/
├── .venv/              # Виртуальное окружение
├── allure-results/     # Результаты тестов для Allure
├── objects/            # Модули для API запросов
│   └── github_api.py   # Методы API (search, create, delete)
├── pages/              # Page Object для UI
│   ├── github_login_page.py
│   └── github_main_page.py
├── test/               # Тестовые сценарии
│   ├── test_api.py     # Тесты API
│   └── test_ui.py      # Тесты UI
├── conftest.py         # Фикстуры pytest
├── pytest.ini          # Конфигурация pytest (маркеры)
├── requirements.txt    # Зависимости проекта
└── .env                # Файл с переменными окружения (token, credentials)
```

## Как запустить тесты

1. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Запуск тестов:**
   - **Все тесты:**
     ```bash
     pytest --alluredir=allure-results
     ```
   - **Только API-тесты:**
     ```bash
     pytest -m api --alluredir=allure-results
     ```
   - **Только UI-тесты:**
     ```bash
     pytest -m ui --alluredir=allure-results
     ```

3. **Просмотр отчета Allure:**
   ```bash
   allure serve allure-results
   ```
Отчет откроется автоматически в браузере

## Технологический стек
- **Python** (pytest)
- **Selenium WebDriver**
- **Requests**
- **Allure Report**

## Ссылка на финальный проект:
 https://studyqa.yonote.ru/share/3b8d064f-6ec4-472d-9828-33bec6ff2e8a
 