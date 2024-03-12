from unittest import mock
import requests
import os
import datetime

response_dict = {"url": {"key": "value"}}


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_requests_get(url):
    if url in response_dict:
        return MockResponse(response_dict[url], 200)
    return MockResponse({"message": "Not found"}, 404)


def test_get(mocker):
    # requests.getの振舞いを別の関数(mocked_requests_get)に置き換え
    mocker.patch("requests.get", side_effect=mocked_requests_get)
    res = requests.get("url")
    assert res.status_code == 200
    assert res.json() == {"key": "value"}

    mocker.patch("requests.get", side_effect=mocked_requests_get)
    res = requests.get("no-url")
    assert res.status_code == 404
    assert res.json() == {"message": "Not found"}


def test_post(mocker):
    # requests.postに対して固定戻り値を登録
    mocker.patch("requests.post", return_value="post_result")
    result = requests.post("arg")
    assert result == "post_result"


def test_env_dict(mocker):
    mocker.patch.dict(
        "os.environ", {"BUCKET_NAME": "test-bucket", "TABLE_NAME": "test-table"}
    )
    assert os.environ.get("BUCKET_NAME") == "test-bucket"
    assert os.environ.get("TABLE_NAME") == "test-table"
    assert os.environ.get("NON_ENV") is None


def test_env_method(mocker):
    # os.environ値をmock化
    def mock_os_environ_get(var: str):
        env = {"BUCKET_NAME": "test-bucket", "TABLE_NAME": "test-table"}
        if var in env:
            return env[var]
        return None

    mocker.patch("os.environ.get", side_effect=mock_os_environ_get)
    assert os.environ.get("BUCKET_NAME") == "test-bucket"
    assert os.environ.get("TABLE_NAME") == "test-table"
    assert os.environ.get("NON_ENV") is None


def test_datetime(mocker):
    # プロパティと関数を両方Mock化
    mocker.patch(
        "datetime.datetime",
        **{
            "year": 2000,
            "year_method.return_value": 3000,
        }
    )
    assert datetime.datetime.year == 2000
    assert datetime.datetime.year_method() == 3000


def test_complicated(mocker):
    # 複雑なMock
    a = 1
    # **内では, return_valueが()となる.
    mocker.patch(
        "datetime.datetime",
        **{"now.return_value.year.multiply_five.return_value.str": "10000"}
    )
    assert datetime.datetime.now().year.multiply_five().str == "10000"
