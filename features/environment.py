from behave import fixture, use_fixture
from django.contrib.auth import get_user_model
from selenium.webdriver import Chrome

User = get_user_model()

@fixture
def browser_chrome(context):
    context.browser = Chrome()
    yield context.browser
    context.browser.quit()


def before_all(context):
    use_fixture(browser_chrome, context)

def before_scenario(context, scenario):
    User.objects.create_user(username='admin', password='admin')