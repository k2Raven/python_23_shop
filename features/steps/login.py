from time import sleep

from behave import given, when, then
from selenium.webdriver.common.by import By


@given('Я открыл страницу "Входа"')
def open_login_page(context):
    context.browser.get(context.get_url('/accounts/login/'))


@when('Я ввожу текст "{text}" в поле "{name}"')
def enter_text(context, text, name):
    context.browser.find_element(By.NAME, name).send_keys(text)

@when('Я отправляю форму')
def submit_form(context):
    form = context.browser.find_element(By.CSS_SELECTOR, 'form')
    form.submit()


@then('Я должен быть на главной странице')
def should_be_at_main(context):
    assert context.browser.current_url == context.get_url('/')


@then("Я должен быть на странице входа")
def should_be_at_login(context):
    assert context.browser.current_url == context.get_url('/accounts/login/')


@then('Я должен видеть сообщение об ошибке с текстом "{text}"')
def see_error_with_text(context, text):
    error = context.browser.find_element(By.CLASS_NAME, 'form-error')
    print(error.text)
    assert error.text == text
