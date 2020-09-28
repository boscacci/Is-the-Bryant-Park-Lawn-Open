import os
import sys
from io import StringIO

import boto3
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

from vizgen_helpers import make_uptime_plotly_fig
from viz_html_gen import generate_vizgen_html

hostname = os.getenv("DB_HOST")
if not hostname:
    print("ERROR: No DB hostname found in env")
    sys.exit()


def lambda_handler(event, context):
    df = get_all_lawn_rows()

    time_EST = (
        pd.to_datetime(df.iloc[-1]["utc_time"], unit="ms")
        .tz_localize("utc")
        .tz_convert("US/Eastern")
    ).strftime("%B %d, %Y, %I:%M %p")

    print(f"current time is {time_EST}.")

    # write_to_bucket(df) # (For making a local debug CSV)

    # Create a plotly fig object, write as json to s3
    uptime_fig = make_uptime_plotly_fig(df)
    write_fig_to_bucket(uptime_fig)

    # The HTML will get the json data injected by some ES6
    stats_page_html = generate_vizgen_html(time_EST)

    # Has to be written to the bucket of course
    write_stats_html_to_bucket(stats_page_html)

    return {"statusCode": 200}


def get_all_lawn_rows():
    print(f"RDS hostname: {hostname}")
    engine = make_db_connection()
    qry = "SELECT * FROM lawn"
    print("Loading all rows...")
    df = pd.read_sql_query(qry, engine, parse_dates={"utc_time": "ms"})
    print("Got all rows.")
    return df


def write_fig_to_bucket(uptime_fig):
    print("Writing fig data as JSON to bucket...")
    bucket = "isthebryantparklawnopen.com"
    s3 = boto3.resource("s3")
    s3_object = s3.Object(bucket, "plots/uptime_heatmap.json")
    s3_object.put(Body=uptime_fig.to_json())
    print("Wrote fig json to bucket.")


def write_stats_html_to_bucket(stats_html):
    """
    Actually create the stats html page for site
    """
    bucket = "isthebryantparklawnopen.com"
    print("Writing second HTML page to ITBPLO bucket...")
    s3_resource = boto3.resource("s3")
    s3_resource.Object(bucket, "stats.html").put(Body=stats_html)
    print("Wrote stats page to s3.")


def write_to_bucket(df):
    """
    Simply write a csv to a bucket for local debug
    """
    bucket = "lawn-plotly-viz"
    print("Writing dataframe to s3 bucket...")
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource("s3")
    s3_resource.Object(bucket, "lawn.csv").put(Body=csv_buffer.getvalue())
    print("Wrote to s3.")


def make_db_connection():
    try:
        db_uri = f"postgres+psycopg2://lawn_admin:lawn_password@{hostname}:6543/lawndb"
        engine = create_engine(db_uri, echo=False)

    except:
        print("ERROR: Couldn't connect to lawn RDS DB.")
        sys.exit()

    return engine
