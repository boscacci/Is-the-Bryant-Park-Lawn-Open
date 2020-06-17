from lawn_scraper import get_lawn_status
import boto3
from time import sleep
import os


def populate_status_strings():
    lawn_status_strings = ("", "")
    while lawn_status_strings == ("", ""):
        lawn_status_strings = get_lawn_status()
    return lawn_status_strings


def write_html():
    lawn_status_strings = populate_status_strings()
    open_photo_url = (
        "https://s3.amazonaws.com/isthebryantparklawnopen.com/bplawn_open.jpg"
    )
    closed_photo_url = (
        "https://s3.amazonaws.com/isthebryantparklawnopen.com/bplawn_closed.jpg"
    )
    photo_url = (
        open_photo_url if "open" in lawn_status_strings[0] else closed_photo_url
    )

    open_bool = "open" in lawn_status_strings[0]

    html_str = f"""<!doctype html>
    <html lang="en">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    <h1 align="center"><font size='36'>
        {'YUP' if open_bool else 'NOPE'}
    </font></h1>
    
    <p align='center'>
        {lawn_status_strings[1] if not open_bool else ''}
    </p>

    <!-- I <3 Catherine!! -->
    
    <div align='center'>
       <img src={photo_url}>
    </div>
    
    </html>
    """
    return html_str


def upload_file(html_str):
    """Upload a file to an S3 bucket

    :file_name: File to upload
    :bucket: Bucket to upload to
    :object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    client = boto3.client("s3")

    response = client.put_object(
        Bucket="isthebryantparklawnopen.com",
        Body=html_str,
        Key="index.html",
        ContentType="text/html",
    )


def lambda_handler(a, b):
    html_str = write_html()
    upload_file(html_str)
