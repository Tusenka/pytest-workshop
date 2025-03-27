import pytest


@pytest.fixture(scope="session")
def config():
    return {
            'base_url': 'https://www.saucedemo.com',
            'login_page': '/',
            'inventory_page': 'inventory.html',
            'login_id': 'user-name',
            'password_id': 'password',
            'button_id': 'login-button',
            }
