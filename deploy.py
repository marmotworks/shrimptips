#!/usr/bin/env python3
"""
Deployment script for ShrimpTips CloudFormation stack.
This script packages the Lambda functions and deploys the CloudFormation template.
"""
import sys
import os
import boto3
import zipfile
import tempfile
from pathlib import Path
from botocore.exceptions import ClientError

def create_lambda_package(function_name, source_file):
    """Create a deployment package for a Lambda function."""
    print(f"Creating deployment package for {function_name}...")
    
    # Create a temporary zip file
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add the Python file to the zip
            zipf.write(source_file, Path(source_file).name)
        
        return temp_zip.name

def update_lambda_function(function_name, zip_file_path):
    """Update a Lambda function with new code."""
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    try:
        with open(zip_file_path, 'rb') as zip_file:
            lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_file.read()
            )
        print(f"Successfully updated {function_name}")
        return True
    except ClientError as e:
        print(f"Error updating {function_name}: {e}")
        return False

def deploy_cloudformation_stack(stack_name, template_file, hosted_zone_id=None):
    """Deploy or update the CloudFormation stack."""
    cf_client = boto3.client('cloudformation', region_name='us-east-1')
    
    # Read the template
    with open(template_file, 'r') as f:
        template_body = f.read()
    
    # Prepare parameters
    parameters = []
    if hosted_zone_id:
        parameters.append({
            'ParameterKey': 'HostedZoneId',
            'ParameterValue': hosted_zone_id
        })
    
    try:
        # Check if stack exists
        try:
            cf_client.describe_stacks(StackName=stack_name)
            stack_exists = True
        except ClientError:
            stack_exists = False
        
        if stack_exists:
            print(f"Updating existing stack: {stack_name}")
            response = cf_client.update_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            operation = 'UPDATE'
        else:
            print(f"Creating new stack: {stack_name}")
            response = cf_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            operation = 'CREATE'
        
        print(f"Stack {operation} initiated. Stack ID: {response.get('StackId', 'N/A')}")
        
        # Wait for stack operation to complete
        print("Waiting for stack operation to complete...")
        waiter_name = 'stack_update_complete' if stack_exists else 'stack_create_complete'
        waiter = cf_client.get_waiter(waiter_name)
        waiter.wait(StackName=stack_name)
        
        print(f"Stack {operation.lower()} completed successfully!")
        
        # Get stack outputs
        response = cf_client.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0].get('Outputs', [])
        
        print("\nStack Outputs:")
        for output in outputs:
            print(f"  {output['OutputKey']}: {output['OutputValue']}")
        
        return True
        
    except ClientError as e:
        print(f"Error with CloudFormation stack: {e}")
        return False

def main():
    """Main deployment function."""
    print("🦐 ShrimpTips Deployment Script")
    print("=" * 40)
    
    # Set up AWS credentials
    try:
        # Test AWS credentials
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"Deploying with AWS Account: {identity['Account']}")
        print("Using region: us-east-1")
    except Exception as e:
        print(f"Error with AWS credentials: {e}")
        sys.exit(1)
    
    stack_name = "shrimptips-webapp"
    
    # Deploy CloudFormation stack first
    print("\n1. Deploying CloudFormation stack...")
    template_file = Path("templates/shrimptips-stack.yaml")
    
    if not template_file.exists():
        print(f"Error: Template file {template_file} not found!")
        sys.exit(1)
    
    # For now, deploy without custom domain (hosted zone ID can be added later)
    success = deploy_cloudformation_stack(stack_name, str(template_file))
    
    if not success:
        print("CloudFormation deployment failed!")
        sys.exit(1)
    
    # Update Lambda functions with actual code
    print("\n2. Updating Lambda functions with code...")
    
    # Package and update poster generator function
    poster_zip = create_lambda_package("poster_generator", "lambdas/poster_generator.py")
    success1 = update_lambda_function(f"{stack_name}-poster-generator", poster_zip)
    os.unlink(poster_zip)  # Clean up temp file
    
    # Package and update web interface function
    web_zip = create_lambda_package("web_interface", "lambdas/web_interface.py")
    success2 = update_lambda_function(f"{stack_name}-web-interface", web_zip)
    os.unlink(web_zip)  # Clean up temp file
    
    if success1 and success2:
        print("\n✅ Deployment completed successfully!")
        print("\nYour ShrimpTips webapp is now live!")
        
        # Get the API Gateway URL
        cf_client = boto3.client('cloudformation', region_name='us-east-1')
        response = cf_client.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0].get('Outputs', [])
        
        for output in outputs:
            if output['OutputKey'] == 'ApiGatewayUrl':
                print(f"\n🌐 Access your webapp at: {output['OutputValue']}")
                break
    else:
        print("\n❌ Lambda function updates failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()