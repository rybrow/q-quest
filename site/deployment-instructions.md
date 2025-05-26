# Q-Quest! Website Deployment Instructions

This document provides step-by-step instructions for deploying the Q-Quest! website using AWS CloudFormation, S3, CloudFront, and Route53.

## Prerequisites

1. An AWS account with appropriate permissions
2. AWS CLI installed and configured
3. A registered domain name
4. A Route53 hosted zone for your domain
5. The website files in the `site` directory

## Deployment Steps

### 1. Deploy the CloudFormation Stack

```bash
aws cloudformation create-stack \
  --stack-name q-quest-website \
  --template-body file://cloudformation-template.yaml \
  --parameters \
    ParameterKey=DomainName,ParameterValue=qquest.example.com \
    ParameterKey=HostedZoneId,ParameterValue=Z1234567890ABC \
    ParameterKey=CreateWWWAlias,ParameterValue=true \
  --capabilities CAPABILITY_IAM
```

Replace:
- `qquest.example.com` with your actual domain name
- `Z1234567890ABC` with your actual Route53 hosted zone ID

### 2. Wait for Stack Creation

The stack creation will take some time (15-30 minutes) primarily due to the SSL certificate validation. You can monitor the progress in the AWS CloudFormation console or using the AWS CLI:

```bash
aws cloudformation describe-stacks --stack-name q-quest-website
```

### 3. Validate Certificate (if needed)

If the stack creation is stuck at the certificate creation step, you may need to manually add the DNS validation records. Check the CloudFormation events or the Certificate Manager console for the required validation records.

### 4. Upload Website Content

Once the stack is created successfully, upload your website content to the S3 bucket. The bucket name will be the same as your domain name:

```bash
aws s3 sync ./site s3://qquest.example.com --delete --exclude "cloudformation-template.yaml" --exclude "deployment-instructions.md" --exclude "README.md"
```

### 5. Invalidate CloudFront Cache

After uploading the content, invalidate the CloudFront cache to ensure the latest content is served:

```bash
# Get the distribution ID from the stack outputs
DISTRIBUTION_ID=$(aws cloudformation describe-stacks --stack-name q-quest-website --query "Stacks[0].Outputs[?OutputKey=='CloudFrontDistributionId'].OutputValue" --output text)

# Create an invalidation
aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/*"
```

### 6. Verify the Website

Open your browser and navigate to your domain (e.g., https://qquest.example.com). The website should be accessible over HTTPS.

## Updating the Website

To update the website content, simply upload the new files to the S3 bucket and invalidate the CloudFront cache:

```bash
# Upload new content
aws s3 sync ./site s3://qquest.example.com --delete --exclude "cloudformation-template.yaml" --exclude "deployment-instructions.md" --exclude "README.md"

# Invalidate cache
aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/*"
```

## Cleanup

If you want to remove the website and all associated resources, delete the CloudFormation stack:

```bash
aws cloudformation delete-stack --stack-name q-quest-website
```

Note: This will delete the S3 bucket and all its contents, the CloudFront distribution, the SSL certificate, and the DNS records. The domain itself and the Route53 hosted zone will remain intact.

## Troubleshooting

### Certificate Validation Issues

If the certificate validation fails, ensure that:
1. The Route53 hosted zone ID is correct
2. The domain name is correctly specified
3. The DNS propagation has completed (can take up to 48 hours in some cases)

### S3 Access Issues

If you encounter permission errors when uploading to S3, check that:
1. Your AWS CLI is properly configured with the correct credentials
2. The IAM user/role has the necessary S3 permissions

### CloudFront Issues

If the website is not accessible or showing outdated content:
1. Verify that the CloudFront distribution is deployed (Status: Deployed)
2. Check that the invalidation has completed
3. Clear your browser cache

### DNS Issues

If the website is not accessible at your domain:
1. Verify that the DNS records have been created in Route53
2. Check that the DNS propagation has completed (can take up to 48 hours)
3. Use tools like `dig` or `nslookup` to verify the DNS resolution
