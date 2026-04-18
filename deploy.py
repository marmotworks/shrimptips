#!/usr/bin/env python3
"""
Deployment script for ShrimpTips CloudFormation stack.
This script packages the Lambda functions and deploys the CloudFormation template.
"""
import sys
import os
import time
import boto3
import zipfile
import tempfile
from pathlib import Path
from botocore.exceptions import ClientError

import config

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
    lambda_client = boto3.client('lambda', region_name=config.AWS_REGION)
    
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

def delete_legacy_cloudfront_distribution():
    """Delete the legacy CloudFront distribution.
    
    Before deleting, removes the shrimp.tips CNAME alias to free it for
    the new CloudFormation-managed distribution.
    """
    print("\n1. Cleaning up legacy CloudFront distribution...")
    cloudfront = boto3.client('cloudfront', region_name=config.AWS_REGION)
    
    try:
        dist = cloudfront.get_distribution(Id=config.LEGACY_CLOUDFRONT_DISTRIBUTION_ID)
        dist_config = dist['Distribution']['DistributionConfig']
        etag = dist['ETag']
        
        # Remove shrimp.tips from aliases to free the CNAME
        aliases = dist_config.get('Aliases', {}).get('Items', [])
        original_aliases = list(aliases)
        
        if 'shrimp.tips' in aliases:
            aliases.remove('shrimp.tips')
            print(f"  Removed shrimp.tips alias from distribution (was: {original_aliases})")
        else:
            print(f"  shrimp.tips alias not found in distribution aliases: {aliases}")
        
        dist_config['Aliases'] = {'Quantity': len(aliases), 'Items': aliases}
        
        # Update the distribution to remove the alias
        cloudfront.update_distribution(
            Id=config.LEGACY_CLOUDFRONT_DISTRIBUTION_ID,
            DistributionConfig=dist_config,
            IfMatch=etag
        )
        print("  Updated distribution to remove shrimp.tips alias")
        
        # Wait a moment for the alias update to propagate
        time.sleep(5)
        
        # Re-fetch the ETag since update_distribution generates a new one
        dist = cloudfront.get_distribution(Id=config.LEGACY_CLOUDFRONT_DISTRIBUTION_ID)
        etag = dist['ETag']
        
        # Delete the distribution
        cloudfront.delete_distribution(Id=config.LEGACY_CLOUDFRONT_DISTRIBUTION_ID, IfMatch=etag)
        print(f"  Deleted legacy CloudFront distribution {config.LEGACY_CLOUDFRONT_DISTRIBUTION_ID}")
        
        # Wait for deletion to complete (max ~5 minutes)
        print("  Waiting for distribution deletion to complete...")
        waiter = cloudfront.get_waiter('distribution_deleted')
        waiter.wait(Id=config.LEGACY_CLOUDFRONT_DISTRIBUTION_ID, WaiterConfig={'Delay': 10, 'MaxAttempts': 30})
        print("  Legacy CloudFront distribution deleted successfully")
        
    except ClientError as e:
        error_code = e.response['Error']['Code'] if 'Error' in e.response else ''
        if error_code == 'NoSuchDistribution':
            print("  Legacy CloudFront distribution already deleted")
        elif error_code == 'PreconditionFailed':
            print(f"  Precondition error (etag mismatch): {e}")
            print("  Attempting to re-fetch and delete...")
            try:
                dist = cloudfront.get_distribution(Id=config.LEGACY_CLOUDFRONT_DISTRIBUTION_ID)
                dist_config = dist['Distribution']['DistributionConfig']
                etag = dist['ETag']
                cloudfront.delete_distribution(Id=config.LEGACY_CLOUDFRONT_DISTRIBUTION_ID, IfMatch=etag)
                print(f"  Deleted legacy CloudFront distribution {config.LEGACY_CLOUDFRONT_DISTRIBUTION_ID}")
                waiter = cloudfront.get_waiter('distribution_deleted')
                waiter.wait(Id=config.LEGACY_CLOUDFRONT_DISTRIBUTION_ID, WaiterConfig={'Delay': 10, 'MaxAttempts': 30})
                print("  Legacy CloudFront distribution deleted successfully")
            except ClientError as e2:
                print(f"  Could not delete legacy distribution: {e2}")
        else:
            print(f"  Error accessing legacy distribution: {e}")

def deploy_cloudformation_stack(stack_name, template_file, hosted_zone_id=None):
    """Deploy or update the CloudFormation stack."""
    cf_client = boto3.client('cloudformation', region_name=config.AWS_REGION)
    
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
        if 'No updates are to be performed' in str(e):
            print("No updates needed for CloudFormation stack.")
            return True
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
        print(f"Using region: {config.AWS_REGION}")
    except Exception as e:
        print(f"Error with AWS credentials: {e}")
        sys.exit(1)
    
    stack_name = config.STACK_NAME
    hosted_zone_id = config.HOSTED_ZONE_ID
    
    # Step 1: Delete legacy CloudFront distribution (if it exists)
    # This frees the shrimp.tips CNAME for the new CloudFormation-managed distribution
    delete_legacy_cloudfront_distribution()
    
    # Step 2: Deploy CloudFormation stack
    print("\n2. Deploying CloudFormation stack...")
    template_file = Path("templates/shrimptips-stack.yaml")
    
    if not template_file.exists():
        print(f"Error: Template file {template_file} not found!")
        sys.exit(1)
    
    success = deploy_cloudformation_stack(stack_name, str(template_file), hosted_zone_id)
    
    if not success:
        print("CloudFormation deployment failed!")
        sys.exit(1)
    
    # Step 3: Update Lambda functions with actual code
    print("\n3. Updating Lambda functions with code...")
    
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
        
        # Get CloudFront domain from stack outputs
        cf_client = boto3.client('cloudformation', region_name=config.AWS_REGION)
        response = cf_client.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0].get('Outputs', [])
        
        cloudfront_domain = None
        for output in outputs:
            if output['OutputKey'] == 'CloudFrontDomain':
                cloudfront_domain = output['OutputValue']
                break
        
        if cloudfront_domain and cloudfront_domain != 'Not configured - no HostedZoneId provided':
            print(f"\n🌐 Access your webapp at: https://shrimp.tips")
            print(f"   CloudFront domain: {cloudfront_domain}")
        else:
            print(f"\n🌐 Access your webapp at: https://shrimp.tips")
            print("   Note: CloudFront not configured - provide HostedZoneId for custom domain support")
    else:
        print("\n❌ Lambda function updates failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
