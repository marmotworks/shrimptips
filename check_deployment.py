import boto3
import hashlib
import zipfile
import tempfile
import os
from pathlib import Path
from botocore.exceptions import ClientError

def get_file_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def create_lambda_package_sha256(source_file):
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(source_file, Path(source_file).name)
        sha256 = get_file_sha256(temp_zip.name)
        os.unlink(temp_zip.name)
        return sha256

def check_deployment():
    region = 'us-east-1'
    stack_name = "shrimptips-webapp"
    cf_client = boto3.client('cloudformation', region_name=region)
    lambda_client = boto3.client('lambda', region_name=region)

    print(f"--- Checking deployment for stack: {stack_name} ---")

    # 1. Check CloudFormation Stack
    try:
        stack = cf_client.describe_stacks(StackName=stack_name)['Stacks'][0]
        print(f"Stack Status: {stack['StackStatus']}")
        print(f"Stack Creation Time: {stack['CreationTime']}")
    except ClientError as e:
        print(f"Error describing stack: {e}")
        return

    # 2. Check Lambda Functions
    lambdas_to_check = [
        {"name": f"{stack_name}-poster-generator", "file": "lambdas/poster_generator.py"},
        {"name": f"{stack_name}-web-interface", "file": "lambdas/web_interface.py"},
    ]

    for item in lambdas_to_check:
        print(f"\n--- Checking Lambda: {item['name']} ---")
        try:
            remote_lambda = lambda_client.get_function(FunctionName=item['name'])
            remote_sha256 = remote_lambda['Configuration']['CodeSha256']
            print(f"Remote Code SHA256: {remote_sha256}")
            
            # Calculate local SHA256 (after packaging)
            local_sha256 = create_lambda_package_sha256(item['file'])
            # Note: AWS returns Base64 encoded SHA256, so we might need to handle that.
            # Actually, boto3's get_function returns it as a string.
            # Let's see if we need to base64 decode it.
            import base64
            try:
                decoded_remote_sha256 = base64.b64decode(remote_sha256).hex()
            except Exception:
                decoded_remote_sha256 = remote_sha256 # fallback if it's already hex or something else

            print(f"Local Package SHA256: {local_sha256}")
            
            # We need to be careful: AWS SHA256 is the SHA256 of the ZIP file.
            # Our local_sha256 is also the SHA256 of the ZIP file we just created.
            # Let's re-check the remote_sha256 format.
            
            # If they match (after potentially handling base64/hex), then it's up to date.
            # Wait, AWS returns the SHA256 in a specific way.
            # According to documentation, it's the SHA256 of the deployment package.
            
            # Let's just print them and compare.
            if decoded_remote_sha256 == local_sha256:
                print("✅ Match! Lambda is up to date.")
            else:
                print("❌ Mismatch! Lambda is NOT up to date.")
                
        except ClientError as e:
            print(f"Error getting Lambda function: {e}")

if __name__ == "__main__":
    check_deployment()
