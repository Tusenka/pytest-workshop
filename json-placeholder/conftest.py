import pytest


@pytest.fixture(scope="session")
def config():
    return {'base_url': 'https://dummyjson.com', 'posts_link': 'posts'}
