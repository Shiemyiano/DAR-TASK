# DAR-TASK
# Scenario 1: IoT Integration with OPC-UA Simulator

## Objective
To connect to an OPC-UA simulator server, retrieve sensor data, transform it into JSON format, and publish it to an IoT platform via MQTT.

---

## Architecture Overview:

### OPC-UA Clients:
- **opc-clientwrite**: Writes data to the OPC-UA server.
- **opc-clientread**: Reads data from the OPC-UA server and sends it to the MQTT broker.

### MQTT Broker:
Handles message transmission between devices/services.

### Node-RED:
Subscribes to MQTT messages and provides a dashboard for monitoring or further processing.

---

## Detailed Workflow:

### Step 1: Send Random Data to OPC-UA Server
- **File**: `clientwrite.py`
- **Purpose**: Send random temperature and humidity data to the OPC-UA server.
- **URL**: `opc.tcp://localhost:62640/IntegrationObjects/ServerSimulator`
- **Module**: `opcua`

### Step 2: Data Collection by OPC-UA Server
- The OPC-UA server simulator collects the data and makes it available upon request.

### Step 3: Fetch Data from OPC-UA Server
- **File**: `clientread.py`
- **Libraries**: `opcua`, `json`, `paho.mqtt`
- **Connect URL**: `opc.tcp://localhost:62640/IntegrationObjects/ServerSimulator`
- **Node IDs**: 
  - Temperature: `tag7`
  - Humidity: `tag6`
- **SubHandler Class**: Subscribes to updates or changes from sensors.
- **Workflow**:
  1. Fetch data from the server.
  2. Convert data to JSON format.
  3. Publish data via MQTT:
     - **Topic**: `sensor/data`
     - **Port**: `1883`

### Step 4: Consume Data in IoT Platform
- **Tool**: Node-RED
- **Flow**: `mqtt-in` >> `debug`

### Step 5: Containerize the Project
- **Dockerfiles**:
  - Create Dockerfiles for `clientwrite.py` and `clientread.py` using the `python:3.9-slim` image.
- **Docker Compose**:
  - Define a setup with the following services:
    1. MQTT Broker
    2. OPC-UA Client Write
    3. OPC-UA Client Read
    4. Node-RED

---

## GitHub Repository
[Project Link](https://github.com/Shiemyiano/DAR-TASK.git)
