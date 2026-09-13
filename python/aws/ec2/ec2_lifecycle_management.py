import boto3
import subprocess

region = "ap-south-1"
tag_key = "Environment"
tag_value = "dev"
action = "stop"

ec2 = boto3.client("ec2", region_name = region)

if action == "stop":
    target_state = "running"
else:
    target_state = "stopped"

response = ec2.describe_instances(
    Filters = [
        {"Name": f"{tag_key}", "Values": "[tag_value]"},
        {"Name": "instance-state-name", "Values": [target_state]}
    ]
)

instance_ids = []
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instance_ids.append(instance["InstanceId"])

if not instance_ids:
    print(f"No instances found with tag {tag_key} & {tag_value}")
else:
    print(f"Instances to {action}: {instance_ids}")
    if action == "stop":
        ec2.stop_instances(InstanceIds=instance_ids)
    else:
        ec2.start_instances(InstanceIds=instance_ids)