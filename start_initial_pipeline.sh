#!/bin/bash
# Wait for Mage to be fully operational
echo "Waiting for Mage to start..."
sleep 30  # Adjust the sleep duration as necessary

# Trigger the Mage pipeline via API
echo "Triggering the Mage pipeline..."
curl -X POST http://localhost:6789/api/pipeline_schedules/3/pipeline_runs/bafc3dde46ef4a4b8c813ada85db1e41 \
  --header 'Content-Type: application/json' \
  --data '{"pipeline_run": {"variables": {"key": "value"}}}'
