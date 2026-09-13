import boto3
import subprocess

ec2 = ec2.client("ec2", region_name="ap-south-1")
response = ec2.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["instances"]:
        instance_id = instance["InstanceId"]
        instance_type = instance["InstanceType"]
        state = instance["State"]["Name"]
        private_ip = instance.get("PrivateIpAddress", "N/A")
        public_ip = instance.get("PublicIpAddress", "N/A")

        name = "N/A"
        for tag in instance.get("Tags", []):
            if tag["Key"] == "Name":
                name = tag["Value"]
        
        print(f"Instance ID: {instance_id},
                Instance Name: {name},
                Instance Type: {instance_type},
                Public IP: {public_ip},
                Private IP: {private_ip}")