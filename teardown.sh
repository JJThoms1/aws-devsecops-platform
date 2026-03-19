#!/bin/bash
set -e
echo "Tearing down DevSecOps platform..."

aws ecr delete-repository --repository-name devsecops-app --force --region us-east-1 2>/dev/null || true

cd "$(dirname "$0")/terraform"
terraform destroy -var="alert_email=${1:-hello@jhumari.com}" -auto-approve

DETECTOR_ID=$(aws guardduty list-detectors --region us-east-1 --query "DetectorIds[0]" --output text 2>/dev/null)
if [ "$DETECTOR_ID" != "None" ] && [ -n "$DETECTOR_ID" ]; then
  aws guardduty delete-detector --detector-id $DETECTOR_ID --region us-east-1
fi

echo "Done."
