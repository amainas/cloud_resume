import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("VisitorCounter")

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)  # Convert Decimal to int
    raise TypeError

def lambda_handler(event, context):
    try:
        response = table.update_item(
            Key={"id": "counter"},
            UpdateExpression="ADD #cnt :inc",
            ExpressionAttributeNames={"#cnt": "count"},
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW",
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response["Attributes"], default=decimal_default)
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
