import json
import pandas as pd
import psycopg2
import boto3

client = boto3.client("lambda")


def lambda_handler(event, context):

    parsed_data = scrape_and_parse()

    return {
        "statusCode": 200,
        "body": parsed_data,
    }


def scrape_and_parse():
    scraper_response = client.invoke(
        FunctionName="LambdaLawnScraperFunction",
        InvocationType="RequestResponse",
    )

    scraped_data = dict(
        json.loads(scraper_response["Payload"].read().decode("utf-8"))["body"]
    )

    parser_response = client.invoke(
        FunctionName="LambdaLawnParserFunction",
        InvocationType="RequestResponse",
        Payload=bytes(json.dumps(scraped_data), encoding="utf8"),
    )

    parsed_data = dict(
        json.loads(parser_response["Payload"].read().decode("utf-8"))["body"]
    )["body"]

    return parsed_data
