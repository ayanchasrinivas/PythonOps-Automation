import boto3
import subprocess

region = "ap-south-1"
unused_count = 0

ec2 = ec2.client("ec2", region_name=region)
response = ec2.describe_addresses()

print("Public IP | Allocation ID")
print("-" * 40)

for address in response["Addresses"]:
    if "InstanceId" not in address and "NetworkInterfaceId" not in address:
        public_ip = address["PublicIp"]
        allocation_id = address["AllocationId"]
        print(f"{public_ip} | {allocation_id}")
        unused_count += 1

if unused_count == 0:
    print("No unused Elastic IP addresses found")
else:
    print(f"{unused_count} unreleased Elastic IP addresses are found - consider releasing them")