variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "devsecops"
}

variable "budget_limit" {
  description = "Monthly budget limit in USD"
  type        = string
  default     = "10"
}

variable "alert_email" {
  description = "Email address for budget and security alerts"
  type        = string
}
