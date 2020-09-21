import os, sys

# import boto3
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

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

    return {"statusCode": 200}


def update_s3_status(last_2_rows):
    print("Attempting some s3 puts.")


def update_required(last_2_rows):
    statuses = last_2_rows.lawn_open
    current_status = "open" if statuses[0] == True else "closed"
    if statuses[1] != statuses[0]:
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
