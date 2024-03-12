import sys, os, json, pytest, boto3
from moto import mock_aws
from src.dynamo_api import *

dirname = os.path.dirname(__file__)
TABLE_DEF_FILE = os.path.join(dirname, "test_data/table_def.json")
TABLE_DATA_FILE = os.path.join(dirname, "test_data/table_data.json")
_table_name = "test_table"


@pytest.fixture(autouse=True, scope="module")
def setup_ddb():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")

        # テーブルの作成
        with open(TABLE_DEF_FILE) as f:
            table_def = json.load(f)
        dynamodb.create_table(
            TableName=_table_name,
            **table_def,
        )

        # テーブルにデータを投入
        with open(TABLE_DATA_FILE) as f:
            data_str = f.read()
        data_items = json.loads(data_str)
        table = dynamodb.Table(_table_name)
        for item in data_items:
            table.put_item(Item=item)
        yield


def test_get_item_from_id():
    res = get_item_from_id(_table_name, "1")
    assert res["data"] == "data_01"
