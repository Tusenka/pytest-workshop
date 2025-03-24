import pytest


@pytest.fixture(scope="session")
def config():
    return {'base_url': 'https://jsonplaceholder.typicode.com', 'posts_link': 'posts'}
