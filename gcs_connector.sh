#!/bin/bash

# Specify the URL of the Spark JAR file to download
SPARK_JAR_URL="https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar"

# Specify the name of the Spark JAR file
SPARK_JAR_NAME="gcs-connector-hadoop3-latest.jar"

# Specify the directory where you want to download the Spark JAR file
DOWNLOAD_DIR="./lib/"

# Create the download directory if it doesn't exist
mkdir -p $DOWNLOAD_DIR

# Check if the Spark JAR file already exists
if [ ! -f "$DOWNLOAD_DIR/$SPARK_JAR_NAME" ]; then
    # Download the Spark JAR file using curl
    echo "Downloading Spark JAR file..."
    curl -o "$DOWNLOAD_DIR/$SPARK_JAR_NAME" $SPARK_JAR_URL

    # Check if the download was successful
    if [ $? -eq 0 ]; then
        echo "Spark JAR file downloaded successfully to $DOWNLOAD_DIR"
    else
        echo "Failed to download Spark JAR file"
    fi
else
    echo "Spark JAR file already exists in $DOWNLOAD_DIR"
fi
