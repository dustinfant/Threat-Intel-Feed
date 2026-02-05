#!/bin/bash

PORT=5052
APP_DIR="$(pwd)"
LOG_FILE="$APP_DIR/flask.log"

echo "Stopping any Flask processes running on port $PORT..."

# Kill any process using the port
PIDS=$(lsof -t -i:$PORT)
if [ -n "$PIDS" ]; then
  echo "Killing processes: $PIDS"
  kill -9 $PIDS
else
  echo "No processes found on port $PORT"
fi

# Wait until port is free
echo "Waiting for port $PORT to be released..."
while lsof -i:$PORT >/dev/null 2>&1; do
  sleep 0.5
done

echo "Starting Flask app..."
nohup python3 "$APP_DIR/app.py" > "$LOG_FILE" 2>&1 &
echo "Flask app started on port $PORT. Logs are being written to $LOG_FILE"

