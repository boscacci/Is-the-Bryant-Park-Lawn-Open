from datetime import datetime


def lambda_handler(event, context):
    temp_F = int(event["temp_F"])
    raw_lawn_status = event["raw_lawn_status"]

    binary_lawn_open = raw_to_bool(raw_lawn_status)

    utc_time = datetime.now()
    utc_hour_of_day = utc_time.hour
    utc_weekday = utc_time.weekday()

    payload = dict(
        utc_time=utc_time.strftime("%Y-%m-%d %H:%M:%S+00"),
        lawn_open=str(binary_lawn_open).upper(),
        utc_hour=utc_hour_of_day,
        utc_weekday=utc_weekday,
        temp_F=temp_F,
        original_status=raw_lawn_status,
    )

    return {
        "statusCode": 200,
        "body": payload,
    }


def raw_to_bool(raw_lawn_status):
    lower_lawn_status = raw_lawn_status.lower()
    if "lawn is open" in lower_lawn_status:
        return True
    else:
        return False
