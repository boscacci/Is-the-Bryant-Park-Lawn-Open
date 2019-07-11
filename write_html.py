from lawn_scraper import get_lawn_status
import boto3
from time import sleep

def populate_status_strings():
    lawn_status_strings = ('','')
    while lawn_status_strings == ('',''):
        lawn_status_strings = get_lawn_status()
    return lawn_status_strings

def write_html():
    lawn_status_strings = populate_status_strings()
    open_photo_url = 'https://hesterstreetfair.com/wp-content/uploads/2018/06/bryant-park-lawn.jpg'
    closed_photo_url = 'https://2.bp.blogspot.com/-fQ7baSzx6Y8/VzjvktLC1lI/AAAAAAACmps/b7y0Vv2vn_EHkA-LypxT42brxReH8-lbACKgB/s1600/DSCF8783.jpg'
    photo_url = open_photo_url if 'open' in lawn_status_strings[0] else closed_photo_url
    html_str = f"""
    <!doctype html>
    <html lang="en">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    <br>
    <h1 align="center"><font size='36'>
        {'YUP' if 'open' in lawn_status_strings[0] else 'NOPE'}
    </h1>
    
    <br>
    
    <p>
        {lawn_status_strings[1]}
    </p>
    
    <div align='center'>
       <img src={photo_url}>
    </div>
    
    </html>
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

while True:
    write_html()
    upload_file(file_name='index.html', bucket='isthebryantparklawnopen.com')
    sleep(60)
