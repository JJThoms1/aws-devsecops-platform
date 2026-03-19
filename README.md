# AWS DevSecOps Platform

A production-grade serverless API with security scanning, cost governance, and continuous compliance built into every stage of the pipeline.

## What This Builds

- Python Flask API deployed as a Lambda container image behind API Gateway
- DynamoDB table with encryption at rest and point-in-time recovery
- ECR repository with immutable tags and scan-on-push enabled
- GitHub Actions pipeline with Trivy and checkov blocking on CRITICAL findings
- Infracost posting cost estimates on every pull request
- AWS Security Hub with AWS Foundational Security Best Practices and CIS benchmarks
- AWS Config with rules enforcing encryption, tagging, and public access controls
- GuardDuty for threat detection
- CloudTrail with encrypted S3 delivery for full API audit logging
- AWS Budgets with SNS alerts at 80% and 100% of monthly limit
- CloudWatch alarms for Lambda errors and API Gateway 5XX responses

## Architecture
```
Code push
  → Trivy scan (blocks on CRITICAL CVEs)
  → checkov scan (blocks on insecure IaC)
  → Terraform plan + tflint
  → Docker build + ECR push
  → Trivy scan on built image
  → Terraform apply
  → Lambda update
  → Health check verification
```

## Security Controls

| Control | Tool | What it enforces |
|---|---|---|
| Container CVE scanning | Trivy | Blocks CRITICAL vulnerabilities before push |
| IaC security scanning | checkov | Blocks insecure Terraform before apply |
| Continuous compliance | AWS Config | Encryption, tagging, public access rules |
| Threat detection | GuardDuty | Malicious activity and anomaly detection |
| Security findings | Security Hub | CIS and AWS Foundational benchmarks |
| Audit logging | CloudTrail | Every API call logged to encrypted S3 |

## Cost Governance

| Control | Tool | What it enforces |
|---|---|---|
| PR cost estimates | Infracost | Cost diff on every pull request |
| Monthly budget | AWS Budgets | SNS alert at 80% and 100% of limit |
| Lambda errors | CloudWatch | Alert on error spike |
| API errors | CloudWatch | Alert on 5XX spike |

## Pipeline
```
On every push and PR:
  security-scan → terraform-plan

On merge to main only:
  security-scan → terraform-plan → build-and-push → deploy
```

## Deployment

### Prerequisites
- AWS account with appropriate permissions
- Terraform >= 1.14.0
- GitHub Actions secrets configured

### GitHub Actions Secrets Required

| Secret | Value |
|---|---|
| AWS_ROLE_ARN | IAM role ARN for OIDC |
| ALERT_EMAIL | Email for budget and security alerts |
| INFRACOST_API_KEY | Free key from infracost.io |

### Initial Deploy
```bash
cd terraform
terraform init
terraform apply -var="alert_email=your@email.com"
```

## Architecture Decisions

See [docs/adr.md](docs/adr.md) for all design decisions and trade-off reasoning.

## Author

Jhumari Thomas
AWS Certified Solutions Architect Associate
github.com/JJThoms1
