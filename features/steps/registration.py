from time import sleep

from behave import given, then

from accounts.models import User


@given('Я открыл страницу "Регистрации"')
def open_registration_page(context):
    context.browser.get(context.get_url('/accounts/register/'))

@then("Я должен быть на странице регистрации")
def should_be_at_registration(context):
    sleep(5)
    print(User.objects.count())
    assert context.browser.current_url == context.get_url('/accounts/register/')