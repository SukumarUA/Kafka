# Real-Time Kafka Producer-Consumer Example

This project demonstrates a basic real-time data flow using Apache Kafka with Python producer and consumer applications. It’s built to help you understand how Kafka works — from message publishing to consumption — by running everything locally using Docker and Python.

## Table of Contents

- Overview  
- Prerequisites  
- Setup Instructions  
  - 1. Set Up Kafka Cluster (Docker)  
  - 2. Prepare Python Environment and Code  
- How to Run  
  - 1. Run the Consumer  
  - 2. Run the Producer  
  - 3. Observe the Flow  
- Cleanup  
- Understanding the Setup  
- Additional Insights  

## Overview

This project includes:

- Producer: A Python script that sends messages to a Kafka topic continuously.  
- Consumer: A Python script that listens to the Kafka topic and processes messages in real time.  
- Kafka Cluster: Kafka + ZooKeeper running locally using Docker Compose.

## Prerequisites

Install the following on your system before starting:

- Visual Studio Code (VS Code)  
- Python 3.x  
- Docker Desktop

## Setup Instructions

### 1. Set Up Kafka Cluster (Docker)

- Create a folder for your project, for example: kafka_project  
- Open the folder in VS Code  
- Inside the folder, create a file named: docker-compose.yml  
- Paste the docker-compose content (provided separately) into that file  
- Open a terminal in VS Code and navigate to the project directory  
- Start Kafka and ZooKeeper by running: docker-compose up -d  
- To confirm they are running, run: docker-compose ps  
  - You should see zookeeper and broker in "Up" status

### 2. Prepare Python Environment and Code

- Inside your project folder, create two Python files:
  - kafka_producer.py  
  - kafka_consumer.py  
- Paste the respective producer and consumer Python code into each file  
- In the terminal, install the Kafka client library by running: pip install confluent-kafka

## How to Run

Once Kafka is up and Python dependencies are installed:

### 1. Run the Consumer

- Open a new terminal  
- Run: python kafka_consumer.py  
- The consumer will wait for messages

### 2. Run the Producer

- Open another terminal  
- Run: python kafka_producer.py  
- The producer starts sending messages to Kafka

### 3. Observe the Flow

- Switch to the consumer terminal  
- You’ll see messages appearing in real time as they are produced

## Cleanup

### Stop Python Scripts

- Press Ctrl+C (or Cmd+C on macOS) in both producer and consumer terminals

### Stop Kafka and ZooKeeper

- In your terminal, run: docker-compose down  
- This stops and removes all containers and networks created by Docker Compose

## Understanding the Setup

### Why Use Docker Desktop?

- Quick Setup: Spins up Kafka and ZooKeeper without manual configuration  
- Isolation: Keeps your system clean, avoids conflicts with local tools  
- Consistency: Same setup works across any machine with Docker installed  
- Clean Removal: docker-compose down cleans everything with one command  

### Without Docker?

You would need to:

- Install Java manually  
- Download and extract Kafka and ZooKeeper  
- Manually configure .properties and .cfg files  
- Start services in multiple terminals  
- Troubleshoot environment, ports, paths, and version conflicts

## Additional Insights

- Kafka is Distributed: This project uses a single broker setup, but Kafka scales across multiple brokers in production  
- confluent-kafka Library: Acts as a Python client that handles communication with Kafka  
- localhost:9092: Refers to the Kafka broker running inside a Docker container, mapped to your local machine  
- Real-Time Flow: Producer sends messages continuously, consumer listens and receives them instantly  
- Topic Used: Both scripts use a topic named my_test_topic (you can rename it as needed)  
- Consumer Groups:  
  - Same GROUP_ID → Kafka divides message load across consumers  
  - Different GROUP_IDs → Each group gets a full copy of all messages
