FROM mageai/mageai:0.9.68

ARG PIP=pip3
ARG PYSPARK_HADOOP_VERSION=3
ARG USER_CODE_PATH=/home/src/${PROJECT_NAME}

# Add Debian Bookworm repository
RUN echo 'deb http://deb.debian.org/debian bookworm main' > /etc/apt/sources.list.d/bookworm.list

# Install OpenJDK 17
RUN apt-get update -y && \
    apt-get install -y openjdk-17-jdk

# Remove Debian Bookworm repository
RUN rm /etc/apt/sources.list.d/bookworm.list

RUN ${PIP} install pyspark==3.5.1

# Note: this overwrites the requirements.txt file in your new project on first run. 
# You can delete this line for the second run :) 
COPY requirements.txt ${USER_CODE_PATH}/requirements.txt 

RUN ${PIP} install -r ${USER_CODE_PATH}/requirements.txt

ENV MAGE_DATA_DIR=
