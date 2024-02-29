import boto3


def get_item_from_id(table_name, id):
    table = connect_dynamodb(table_name)
    result = get_item(table, {"id": id})
    return result


def connect_dynamodb(table_name):
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
    print("connected table = " + table_name)
    return dynamodb.Table(table_name)


def get_item(table, kwargs):
    result = table.get_item(Key=kwargs)
    result_item = result.get("Item")
    return result_item
