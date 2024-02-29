import sys
import json
import pytest
from moto import mock_aws
import boto3

sys.path.append("../")
import dynamo_api

TABLE_DEF_FILE = "./test_data/table_def.json"
TABLE_DATA_FILE = "./test_data/table_data.json"


@pytest.fixture(autouse=True, scope="module")
def setup_ddb():
    with mock_aws():
        table_name = "foo"
        dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")

        # テーブルの作成
        with open(TABLE_DEF_FILE) as f:
            foo_table_def = json.load(f)
        dynamodb.create_table(
            TableName=table_name,
            **foo_table_def,
        )

        # テーブルにデータを投入
        with open(TABLE_DATA_FILE) as f:
            data_str = f.read()
        data_items = json.loads(data_str)
        table = dynamodb.Table(table_name)
        for item in data_items:
            table.put_item(Item=item)
        yield


def test_get_item_from_id():
    ret = dynamo_api.get_item_from_id("foo", "1")["data"]
    assert ret == "data_01"
