def load_inventory(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    file = event["Records"][0]["s3"]["object"]["key"]
    print("bucket: " + bucket + ", file: " + file + " received")
    return {
        "statusCode": 200,
        "body": "success",
    }


if __name__ == "__main__":
    load_inventory()
