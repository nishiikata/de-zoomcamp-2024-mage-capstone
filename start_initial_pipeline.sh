#!/bin/bash
# Wait for Mage to be fully operational
echo "Waiting for Mage to start..."
sleep 30  # Adjust the sleep duration as necessary

# Ref: https://docs.mage.ai/api-reference/pipeline-schedules/read-pipeline-schedules
pipeline_api="http://localhost:6789/api/pipeline_schedules"
# Use api_key_query from documentation if necessary
# Local testing as of writing has shown it is not required though :-)
# api_key_query="?api_key=zkWlN0PkIKSN0C11CfUHUj84OT5XOJ6tDZ6bDRO2"

jq_filter='.pipeline_schedules | .[] | select(.name | contains("trigger_initial_pipeline")) | pick(.id, .token) | tostring'

id_and_token=$(curl -X GET "$pipeline_api" | jq -r "$jq_filter")
# Get request with api_key_query
# id_and_token=$(curl -X GET "$pipeline_api$api_key_query" | jq -r "$jq_filter")

id=$(echo $id_and_token | jq -r '.id')
token=$(echo $id_and_token | jq -r '.token')
trigger_url="$pipeline_api/$id/pipeline_runs/$token"

echo 'URL to start "trigger_initial_pipeline" pipeline':
echo $trigger_url

# Trigger the Mage pipeline via API
echo "Triggering the Mage pipeline..."
curl -X POST $trigger_url \
  --header 'Content-Type: application/json' \
  --data '{"pipeline_run": {"variables": {"key": "value"}}}'
