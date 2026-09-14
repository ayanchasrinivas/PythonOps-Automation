import boto3
import subprocess
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
response = s3.list_buckets()

for bucket in response["Buckets"]:
    name = bucket["Name"]

    # Audit begins
    # check whether public access is blocked or not
    try:
        config = s3.get_public_access_block(Bucket=name)["PublicAccessBlockConfiguration"]
        public_blocked = all(config.values())
    except ClientError:
        public_blocked = False

    # check whether versioning is enabled or not.
    versioning_response = s3.get_bucket_versioning(Bucket=name)
    versioning = versioning_response.get("Status", "Disabled")

    # check whether encryption is enabled or not.
    try:
        encryption_response = s3.get_bucket_encryption(Bucket=name)
        encryption = encryption_response.get("Status")
        encryption = "Enabled"
    except ClientError:
        encryption = "Disabled"

    print(f"Bucket: {name} | Public Blocked: {public_blocked} | Versioning: {versioning} | Encryption: {encryption}")

