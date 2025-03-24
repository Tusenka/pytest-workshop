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

    def patch(self, url: str, *, body=None, headers=None):
        if headers is None:
            headers = {"Content-type": "application/json; charset=UTF-8"}
        return requests.patch(url=self._link(url), json=body, headers=headers)

    def post(self, url: str, *, body=None, headers=None):
        if headers is None:
            headers = {"Content-type": "application/json; charset=UTF-8"}
        return requests.patch(url=self._link(url), json=body, headers=headers)

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


    @allure.title("Test update post")
    @allure.epic("Posts")
    @allure.tag("critical_path", "positive")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://jsonplaceholder.typicode.com/posts", name="")
    @allure.issue("JW-1.3.2")
    @pytest.mark.parametrize("method,title,body,userId", [('POST','foo', 'bar', '1'), ('PATCH','foo', 'bar', '1'), ('PATCH', None, 'bar', '2'), ('PATCH', 'foo', None, '1'), ('PATCH', 'foo', 'bar', None), ('PATCH', None, None, None)])
    def test_patch_post(self, api: Api, config: dict, method: str, title: str, body: str, userId: str):
        ibody={}
        if title is not None:
            ibody['title']=title
        if body is not None:
            ibody['body']=body
        if userId is not None:
            ibody['userId']=userId
        if method=='POST':
            result=api.post(f"{config['posts_link']}/1", body=ibody)
        else:
            result=api.patch(f"{config['posts_link']}/1", body=ibody)
        assert result.status_code==200
        post=json.loads(result.text)
        assert body is None and len(post['body'])>0 or post['body']==body
        assert title is None and len(post['title'])>0 or post['title']==title
        assert userId is None and post['userId']>=0 or  post['userId'] == userId
        assert post['id']>=0