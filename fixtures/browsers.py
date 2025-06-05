import pytest
from playwright.sync_api import Playwright, Page
from _pytest.fixtures import SubRequest
import allure

from pages.authentication.registration_page import RegistrationPage


@pytest.fixture
def chromium_page(request: SubRequest, playwright: Playwright) -> Page:  # Добавили аргумент request
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(record_video_dir='./videos')  # Создаем контекст для новой сессии браузера
    context.tracing.start(screenshots=True, snapshots=True, sources=True)  # Включаем трейсинг
    page= context.new_page()

    yield page  # Открываем новую страницу в контексте

    # В данном случае request.node.name содержит название текущего автотеста
    context.tracing.stop(path=f'./tracing/{request.node.name}.zip')  # Сохраняем трейсинг в файл
    browser.close()  # Закрываем браузер

    # Прикрепляем файл с трейсингом к Allure отчету
    allure.attach.file(f'./tracing/{request.node.name}.zip', name='trace', extension='zip')
    # Прикрепляем видео автотеста к Allure отчету
    allure.attach.file(page.video.path(), name='video', attachment_type=allure.attachment_type.WEBM)


@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    registration_page = RegistrationPage(page=page)
    registration_page.visit('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration')
    registration_page.registration_form.fill(email='user.name@gmail.com', username='username', password='password')
    registration_page.click_registration_button()

    context.storage_state(path="browser-state.json")
    browser.close()


@pytest.fixture
def chromium_page_with_state(initialize_browser_state, request: SubRequest, playwright: Playwright) -> Page:  # Добавили аргумент request
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="browser-state.json", record_video_dir='./videos')  # Создаем контекст для новой сессии браузера
    context.tracing.start(screenshots=True, snapshots=True, sources=True)  # Включаем трейсинг
    page = context.new_page()

    yield page  # Открываем новую страницу в контексте

    context.tracing.stop(path=f'./tracing/{request.node.name}.zip')  # Сохраняем трейсинг в файл
    browser.close()  # Закрываем браузер

    # Прикрепляем файл с трейсингом к Allure отчету
    allure.attach.file(f'./tracing/{request.node.name}.zip', name='trace', extension='zip')
    # Прикрепляем видео автотеста к Allure отчету
    allure.attach.file(page.video.path(), name='video', attachment_type=allure.attachment_type.WEBM)