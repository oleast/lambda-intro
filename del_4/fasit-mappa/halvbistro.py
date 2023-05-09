import boto3
# from pprint import pprint
import json
from decimal import Decimal

def load_inventory(event, context):

  s3_client = boto3.client('s3')
  dynamodb_resurce = boto3.resource('dynamodb', region_name='eu-west-1')
  inventory_table = dynamodb_resurce.Table('halvors-halvbistro-inventory')

  bucket = event['Records'][0]['s3']['bucket']['name']
  file = event['Records'][0]['s3']['object']['key']

  raw_content = s3_client.get_object(Bucket=bucket, Key=file)['Body'].read()
  content = json.loads(raw_content)

  # print("bucket: " + bucket + ", file: " + file + " received")
  # pprint(content)

  for item in content:
    item['id'] = item['type'] + '-' + item['name']
    inventory_items = inventory_table.get_item(Key={'id': item['id']})
    print(inventory_items)
    if 'Item' in inventory_items:
      inventory_table.update_item(
        Key={'id': item['id']},
        UpdateExpression='set quantity = quantity + :val',
        ExpressionAttributeValues={':val': Decimal(str(item['quantity']))}
      )
    else:
      inventory_table.put_item(Item=item)

  return {
      "statusCode": 200,
      "body": "success",
  }

if __name__ == '__main__':
  load_inventory()
