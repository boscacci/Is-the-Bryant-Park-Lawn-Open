import sys, os, json

import boto3

import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, DateTime, Boolean

client = boto3.client("lambda")

hostname = os.getenv("DB_HOST")
if not hostname:
    print("ERROR: No DB hostname found in env")
    sys.exit()

try:
    db_uri = (
        f"postgres+psycopg2://lawn_admin:lawn_password@{hostname}:6543/lawndb"
    )
    engine = create_engine(db_uri, echo=True)

except:
    print("ERROR: Couldn't connect to lawn RDS DB.")
    sys.exit()


def lambda_handler(event, context):

    print(f"RDS hostname: {hostname}")

    parsed_data = scrape_and_parse()

    print(f"Parsed data: {parsed_data}")

    write_one_row_to_rds(parsed_data)

    return {"statusCode": 200}


def write_one_row_to_rds(parsed_data):
    row_df = pd.DataFrame.from_dict({k: [v] for k, v in parsed_data.items()})
    row_df.to_sql(
        name="lawn",
        con=engine,
        if_exists="append",
        index=False,
        index_label="utc_time",
        dtype={
            "utc_time": DateTime,
            "lawn_open": Boolean,
            "utc_hour": Integer,
            "utc_weekday": Integer,
            "temp_F": Integer,
            "original_status": Text,
        },
    )

    print("One row written.")


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
    )

    return parsed_data
