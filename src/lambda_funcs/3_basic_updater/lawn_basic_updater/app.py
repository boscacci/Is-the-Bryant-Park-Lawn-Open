import os, sys

import boto3
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

from html_formatter import format_index_html

hostname = os.getenv("DB_HOST")
if not hostname:
    print("ERROR: No DB hostname found in env")
    sys.exit()


def lambda_handler(event, context):

    print(f"RDS hostname: {hostname}")

    engine = make_db_connection()

    qry = "SELECT * FROM lawn ORDER BY utc_time DESC LIMIT 2"

    print("Querying DB...")
    last_2_rows = pd.read_sql_query(qry, engine, parse_dates={"utc_time": "ms"})

    print("DB query success.")
    print(f"Last 2 rows: {last_2_rows.to_json()}")

    if update_required(last_2_rows):
        print("New status detected. Time to update the s3 site.")
        update_s3_status(last_2_rows)
    else:
        print("Status has not changed. No s3 update.")

    # if True:  # For debugging s3 puts even though status hasn't changed
    #     print("Testing write to s3")
    #     update_s3_status(last_2_rows)

    return {"statusCode": 200}


def update_s3_status(last_2_rows):
    index_html = format_index_html(last_2_rows)
    write_to_bucket(index_html)


def write_to_bucket(html_str):
    client = boto3.client("s3")

    print("Writing to s3 bucket...")

    response = client.put_object(
        Bucket="isthebryantparklawnopen.com",
        Body=html_str,
        Key="index.html",
        ContentType="text/html",
    )

    print("Wrote to s3.")


def update_required(last_2_rows):
    statuses = last_2_rows.lawn_open
    current_status = "open" if statuses.iloc[0] == True else "closed"
    if statuses[1] != statuses.iloc[0]:
        print(f"Lawn has changed to {current_status}.")
        return True
    else:
        print(f"Lawn is still {current_status}.")
        return False


def make_db_connection():
    try:
        db_uri = f"postgres+psycopg2://lawn_admin:lawn_password@{hostname}:6543/lawndb"
        engine = create_engine(db_uri, echo=False)

    except:
        print("ERROR: Couldn't connect to lawn RDS DB.")
        sys.exit()

    return engine
