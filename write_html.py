from lawn_scraper import get_lawn_status
import boto3

def populate_status_strings():
    lawn_status_strings = ('','')
    while lawn_status_strings == ('',''):
        lawn_status_strings = get_lawn_status()
    return lawn_status_strings

def write_html():
    lawn_status_strings = populate_status_strings()

    html_str = f"""
    <h1>
        {'YUP' if 'open' in lawn_status_strings[0] else 'NOPE'}
    </h1>
    """

    html_file= open("index.html","w")
    html_file.write(html_str)
    html_file.close()

    return True

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :file_name: File to upload
    :bucket: Bucket to upload to
    :object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ContentType': 'text/html'})
    return True

write_html()
upload_file(file_name='index.html', bucket='ibplo')
