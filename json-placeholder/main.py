import json

import allure
import pytest
import requests


#POM implementation
class Api:
    def __init__(self, config: dict):
        self.base_url=config["base_url"]

    def _link(self, link: str):
        return f"{self.base_url}/{link}"

    def post(self, url: str, *, body=None, headers=None):
        if headers is None:
            headers = {"Content-type": "application/json; charset=UTF-8"}
        return requests.post(url=self._link(url), json=body, headers=headers)

    def get(self, url: str, *, headers=None):
        return requests.post(url=self._link(url), headers=headers)

    def delete(self, url: str, *, headers=None):
        return requests.delete(url=self._link(url), headers=headers)


class TestPost():

    @pytest.fixture(scope="session")
    def api(self, config: dict):
        yield Api(config)


    @allure.title("Test create post ")
    @allure.epic("Posts")
    @allure.tag("critical_path", "positive")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://jsonplaceholder.typicode.com/posts", name="")
    @allure.issue("JW-1.3.1")
    @pytest.mark.parametrize("title,body,userId", [('foo', 'bar', '1'), ('', '', '2')])
    def test_create_post(self, api: Api, config: dict, title: str, body: str, userId: str):
        result=api.post(config["posts_link"]+'/add', body={
                'title': title,
                'body': body,
                'userId': userId
            })
        assert result.status_code==201
        post=json.loads(result.text)
        assert post['body']==body
        assert post['title']==title
        assert post['userId'] == userId
        assert post['id']>=0
        
        
    @allure.title("Test delete post")
    @allure.epic("Posts")
    @allure.tag("critical_path", "positive")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://jsonplaceholder.typicode.com/posts", name="")
    @allure.issue("JW-1.3.2")
    @pytest.mark.parametrize("postId", ['1', '2'])
    def test_delete_post(self, api: Api, config: dict, postId: str):
        result=api.delete(f"{config['posts_link']}/{postId}")
        assert result.status_code==200