import boto3
import subprocess
import datetime

unused_for_days = 90
iam = iam.client("iam")

cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=unused_for_days)
response = iam.list_users()
flagged_count = 0

for user in response["Users"]:
    username = user["UserName"]
    keys_response = iam.list_access_keys(UserName=username)

    for key in keys_response["AccessKeyMetadata"]:
        key_id = key["AccessKeyId"]
        status = key["Status"]

        last_used_response = iam.get_access_key_last_used(AccessKeyId=key_id)
        last_used = last_used_response["AccessKeyLastUsed"].get("LastUsedDate")

        if last_used is None or last_used < cutoff:
            print(f"User: {username}, key: {key_id}, Status: {status}, Last Used: {last_used or 'Never'}")
            flagged_count += 1

if flagged_count == 0:
    print(f"No access keys unused for {unused_for_days}+ days")
else:
    print(f"{flagged_count} keys are flagged, review and rotate the keys")