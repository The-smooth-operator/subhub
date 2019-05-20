import boto3
from mockito import when, unstub

from subhub import secrets
from subhub.cfg import CFG


def test_get_secrets():
    """
    test get_secrets
    """
    response = {
        "ARN": "some-arn",
        "CreatedDate": "some-date",
        "Name": "dev/subhub",
        "ResponseMetadata": {
            "HTTPHeaders": {
                "connection": "keep-alive",
                "content-length": "606",
                "content-type": "application/x-amz-json-1.1",
                "date": "some-date",
                "x-amzn-requestid": "cd15fc38-9b56-443e-9986-f17b56b155a0",
            },
            "HTTPStatusCode": 200,
            "RequestId": "cd15fc38-9b56-443e-9986-f17b56b155a0",
            "RetryAttempts": 0,
        },
        "SecretString": '{"STRIPE_API_KEY":"some-stripe-api-key","PAYMENT_API_KEY":"some-payment-api-key","SUPPORT_API_KEY":"some-support-api-key","BASKET_URI":"some-uri","NEW_RELIC_LICENSE_KEY":"some-nr-license-key","NEW_RELIC_ACCOUNT_ID":"some-nr-account-id","NEW_RELIC_TRUSTED_ACCOUNT_KEY":"some-nr-account-id"}',
        "VersionId": "some-version",
        "VersionStages": ["AWSCURRENT"],
    }

    client = boto3.client(service_name="secretsmanager", region_name="us-west-2")
    when(client).get_secret_value(f"{CFG.APP_DEPENV}/{CFG.APP_PROJNAME}").thenReturn(
        response
    )

    assert (
        secrets.get_secret(f"{CFG.APP_DEPENV}/{CFG.APP_PROJNAME}")["STRIPE_API_KEY"]
        == "some-stripe-api-key"
    )
