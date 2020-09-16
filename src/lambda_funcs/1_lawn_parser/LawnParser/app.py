def lambda_handler(event, context):
    temp_F = int(event["temp_F"])
    raw_lawn_status = event["raw_lawn_status"]

    lawn_open = True if "lawn is open" in raw_lawn_status.lower() else False

    payload = dict(
        lawn_open=lawn_open, temp_F=temp_F, original_status=raw_lawn_status,
    )

    return {
        "statusCode": 200,
        "body": payload,
    }
