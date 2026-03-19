# Architecture Decision Record: AWS DevSecOps Platform

## Decision 1: Serverless over containerised EKS
Lambda + API Gateway was chosen over EKS for this project because costs stay near zero with no idle infrastructure. Lambda scales to zero automatically. This directly demonstrates cost optimisation thinking, which is a key differentiator in the current hiring market.

## Decision 2: Security scanning blocks the pipeline
Trivy and checkov are configured with exit-code: 1 on CRITICAL findings. This means a vulnerable container image or an insecure Terraform resource blocks the deployment entirely. Most junior candidates add security scanning as an optional step. Here it is a hard gate.

## Decision 3: Infracost on every PR
Every pull request receives an automated comment showing the cost difference introduced by the change before it is merged. This mirrors FinOps practices at mature engineering organisations and is a talking point almost no junior candidate can demonstrate from experience.

## Decision 4: Three layers of compliance
AWS Config rules enforce tagging, encryption, and public access controls continuously at the resource level. Security Hub aggregates findings from GuardDuty, Config, and the AWS Foundational Security Best Practices standard into a single dashboard. CloudTrail provides a tamper-evident audit log of every API call. These three layers mirror what a regulated financial services organisation like Fidelity would require.

## Decision 5: OIDC authentication for GitHub Actions
No long-lived AWS credentials are stored in GitHub secrets. GitHub Actions exchanges a short-lived JWT token for temporary AWS credentials via STS. This is the same pattern used across all projects in this portfolio.

## Decision 6: Immutable ECR image tags
ECR is configured with IMMUTABLE image tags. Once an image is pushed with a given SHA tag it cannot be overwritten. This prevents silent supply chain attacks where a known-good image tag is replaced with a malicious one.

## Decision 7: DynamoDB encryption and point-in-time recovery
Both server-side encryption and point-in-time recovery are enabled on the DynamoDB table. This satisfies the encryption-at-rest Config rule and provides a 35-day recovery window for accidental data loss.
