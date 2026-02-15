#!/usr/bin/env python3
"""
S3 Bucket Size Calculator

This script lists all objects in an S3 bucket and calculates the total size in GB.
It uses boto3 to interact with AWS S3 and provides a summary of the bucket contents.

Usage:
    python list_bucket_size.py <bucket_name>

Requirements:
    - boto3 library installed
    - AWS credentials configured (via environment variables, ~/.aws/credentials, or IAM role)
"""

import sys
from typing import List, Tuple, Dict, Any
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def list_bucket_objects(bucket_name: str) -> Tuple[List[Dict[str, Any]], float]:
    """
    List all objects in an S3 bucket and calculate total size.

    Args:
        bucket_name: The name of the S3 bucket to list.

    Returns:
        A tuple containing:
            - List of dictionaries with object information (Key, Size)
            - Total size in gigabytes (GB)

    Raises:
        ClientError: If there's an error accessing the bucket.
        NoCredentialsError: If AWS credentials are not configured.
    """
    s3_client = boto3.client('s3')
    objects: List[Dict[str, Any]] = []
    total_size_bytes: int = 0
    
    try:
        # Use paginator to handle buckets with many objects
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name)
        
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    obj_info = {
                        'Key': obj['Key'],
                        'Size': obj['Size'],
                        'LastModified': obj['LastModified']
                    }
                    objects.append(obj_info)
                    total_size_bytes += obj['Size']
        
        # Convert bytes to gigabytes
        total_size_gb: float = total_size_bytes / (1024 ** 3)
        
        return objects, total_size_gb
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            raise ClientError(
                {'Error': {'Code': 'NoSuchBucket', 'Message': f'Bucket "{bucket_name}" does not exist'}},
                'list_objects_v2'
            )
        elif error_code == 'AccessDenied':
            raise ClientError(
                {'Error': {'Code': 'AccessDenied', 'Message': f'Access denied to bucket "{bucket_name}"'}},
                'list_objects_v2'
            )
        else:
            raise


def main() -> None:
    """Main function to execute the script."""
    if len(sys.argv) != 2:
        print("Usage: python list_bucket_size.py <bucket_name>")
        sys.exit(1)
    
    bucket_name: str = sys.argv[1]
    
    try:
        objects, total_size_gb = list_bucket_objects(bucket_name)
        
        print(f"\nBucket: {bucket_name}")
        print(f"Total objects: {len(objects)}")
        print(f"Total size: {total_size_gb:.2f} GB ({total_size_gb * 1024:.2f} MB)\n")
        
        if objects:
            print("Objects in bucket:")
            for obj in objects:
                size_mb = obj['Size'] / (1024 * 1024)
                print(f"  - {obj['Key']}: {size_mb:.2f} MB (Last modified: {obj['LastModified']})")
        else:
            print("Bucket is empty.")
            
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your AWS credentials.")
        sys.exit(1)
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
