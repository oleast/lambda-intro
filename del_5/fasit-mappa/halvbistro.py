import boto3

# from pprint import pprint
import json
from decimal import Decimal


def load_inventory(event, context):

    s3_client = boto3.client("s3")
    dynamodb_resurce = boto3.resource("dynamodb", region_name="eu-west-1")
    sqs = boto3.resource("sqs", region_name="eu-west-1")

    inventory_table = dynamodb_resurce.Table("halvors-halvbistro-inventory")
    queue = sqs.get_queue_by_name(QueueName="halvbistro-inventory-received")

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    file = event["Records"][0]["s3"]["object"]["key"]

    raw_content = s3_client.get_object(Bucket=bucket, Key=file)["Body"].read()
    content = json.loads(raw_content)

    # print("bucket: " + bucket + ", file: " + file + " received")
    # pprint(content)

    for item in content:
        item["id"] = item["type"] + "-" + item["name"]
        inventory_items = inventory_table.get_item(Key={"id": item["id"]})

        if "Item" in inventory_items:
            inventory_table.update_item(
                Key={"id": item["id"]},
                UpdateExpression="set quantity = quantity + :val",
                ExpressionAttributeValues={":val": Decimal(str(item["quantity"]))},
            )
            if Decimal(inventory_items["Item"]["quantity"]) + item["quantity"] <= 0:
                item["update-type"] = "OUT_OF_STOCK"
            elif Decimal(inventory_items["Item"]["quantity"]) + item["quantity"] >= 50:
                item["update-type"] = "HIGH_STOCK"
            else:
                item["update-type"] = "ITEM_UPDATE"
        else:
            inventory_table.put_item(Item=item)
            item["update-type"] = "NEW_ITEM"
        queue.send_message(MessageBody=json.dumps(item))

    return {
        "statusCode": 200,
        "body": "success",
    }


if __name__ == "__main__":
    load_inventory()
