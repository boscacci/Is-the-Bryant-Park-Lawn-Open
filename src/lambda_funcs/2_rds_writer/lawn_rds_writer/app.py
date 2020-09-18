import sys, os, json

import pandas as pd
import psycopg2
import boto3

client = boto3.client("lambda")

hostname = os.getenv("DB_HOST")
if not hostname:
    print("ERROR: No DB hostname found in env")
    sys.exit()

try:
    conn = psycopg2.connect(
        dbname="lawndb",
        user="lawn_admin",  # Not a secret
        password="lawn_password",  # Not a secret
        host=hostname,
        port=6543,
    )

except:
    print("ERROR: Couldn't connect to RDS instance.")
    sys.exit()


def lambda_handler(event, context):

    print(f"hostname: {hostname}")

    parsed_data = scrape_and_parse()

    return {
        "statusCode": 200,
        "body": parsed_data,
    }


def scrape_and_parse():

    print("starting to scrape...")

    scraper_response = client.invoke(
        FunctionName="LambdaLawnScraperFunction",
        InvocationType="RequestResponse",
    )

    print("Successful scrape.")

    scraped_data = dict(
        json.loads(scraper_response["Payload"].read().decode("utf-8"))["body"]
    )

    parser_response = client.invoke(
        FunctionName="LambdaLawnParserFunction",
        InvocationType="RequestResponse",
        Payload=bytes(json.dumps(scraped_data), encoding="utf8"),
    )

    print("Successful parse.")

    parsed_data = dict(
        json.loads(parser_response["Payload"].read().decode("utf-8"))["body"]
    )["body"]

    return parsed_data
