import pandas as pd


def format_index_html(last_2_rows):
    print("Attempting some s3 puts.")

    latest_row = last_2_rows.iloc[0]

    open_photo_url = "https://s3.amazonaws.com/isthebryantparklawnopen.com/img/bplawn_open.jpg"

    closed_photo_url = "https://s3.amazonaws.com/isthebryantparklawnopen.com/img/bplawn_closed.jpg"

    lawn_is_open = latest_row["lawn_open"] == True

    photo_url = open_photo_url if lawn_is_open else closed_photo_url

    time_EST = (
        pd.to_datetime(latest_row["utc_time"], unit="ms")
        .tz_localize("utc")
        .tz_convert("US/Eastern")
    ).strftime("%B %d, %Y, %r")

    html_str = f"""
    <!doctype html>
    <html lang="en">
    
        <link rel="icon" type="image/png" href="https://s3.amazonaws.com/isthebryantparklawnopen.com/img/fav.png">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
        
        <body>
        
            <h1 align="center" style='font-size:15vw;'>
                {'YUP' if lawn_is_open else 'NOPE'}
            </h1>

            <!-- I <3 Catherine!! -->
            
            <div align='center'>
            <img src={photo_url}>
            </div>

            <br/>

            <p align='center' style='font-size:8vw;'>
                {latest_row['original_status']}
            </p>

            <p align='center'>
                Last updated at {time_EST} EST.
            </p>
        
        </body>

    </html>
    """
    return html_str
