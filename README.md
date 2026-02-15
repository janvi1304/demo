# S3 Bucket Size Calculator

A Python script that lists all objects in an S3 bucket and calculates the total size in GB.

## Features

- Lists all objects in a specified S3 bucket
- Displays each object's name, size, and last modified date
- Calculates and displays total bucket size in GB and MB
- Handles large buckets with pagination
- Comprehensive error handling
- Follows Python best practices with type hints and docstrings

## Requirements

- Python 3.6 or higher
- boto3 library
- AWS credentials configured

## Installation

1. Install boto3:
```bash
pip install boto3
```

2. Configure AWS credentials using one of these methods:
   - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
   - AWS credentials file (`~/.aws/credentials`)
   - IAM role (if running on EC2, Lambda, etc.)

## Usage

```bash
python list_bucket_size.py <bucket_name>
```

Or make it executable and run directly:
```bash
chmod +x list_bucket_size.py
./list_bucket_size.py <bucket_name>
```

## Example Output

```
Bucket: my-example-bucket
Total objects: 42
Total size: 5.67 GB (5811.20 MB)

Objects in bucket:
  - document1.pdf: 2.34 MB (Last modified: 2024-01-15 10:30:00+00:00)
  - image.jpg: 1.56 MB (Last modified: 2024-01-14 09:15:00+00:00)
  ...
```

## Security Best Practices

- Never hardcode AWS credentials in the script
- Use IAM roles with least privilege access
- Ensure the IAM user/role has `s3:ListBucket` and `s3:GetObject` permissions
- Consider using AWS Organizations SCPs for additional security boundaries
