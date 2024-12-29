import time
import json
from opcua import Client, ua
import paho.mqtt.client as mqtt

# Global variable to store the data
data_dict = {}

# OPC UA server details
url = "opc.tcp://host.docker.internal:62640/IntegrationObjects/ServerSimulator"  
temperature_node_id = "ns=2;s=Tag7"  
humidity_node_id = "ns=2;s=Tag6" 

# MQTT settings for local broker
mqtt_broker = "host.docker.internal"  
mqtt_port = 1883           
mqtt_topic = "sensor/data"  

# Define a subscription handler
class SubHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client  # Store MQTT client for publishing
        self.last_temperature = None
        self.last_humidity = None

    def datachange_notification(self, node, val, data):
        """This method is called whenever subscribed data changes."""
        global data_dict  # Declare data_dict as global to modify it

        if node.nodeid.to_string() == temperature_node_id:
            self.last_temperature = val
            print(f"Updated Temperature: {val} °C")
            data_dict['temperature'] = val  # Update global data_dict with temperature data

        elif node.nodeid.to_string() == humidity_node_id:
            self.last_humidity = val
            print(f"Updated Humidity: {val} %")
            data_dict['humidity'] = val  # Update global data_dict with humidity data

        # Convert the updated dictionary to JSON
        json_data = json.dumps(data_dict)
        
        # Publish JSON data to MQTT topic
        self.mqtt_client.publish(mqtt_topic, json_data)
        print(f"Published to MQTT topic '{mqtt_topic}': {json_data}")

# Create a OPC client instance
client = Client(url)
# Create an MQTT client
mqtt_client = mqtt.Client()

try:
    # Connect to the MQTT broker
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    mqtt_client.loop_start()  # Start the MQTT loop to handle background operations
    print(f"Connected to MQTT broker at {mqtt_broker}:{mqtt_port}")

    # Connect to the OPC UA server
    client.connect()
    print("Connected to OPC UA server.")

    # Get the nodes for temperature and humidity
    temperature_node = client.get_node(temperature_node_id)
    humidity_node = client.get_node(humidity_node_id)

    # Create a subscription
    handler = SubHandler(mqtt_client)  # Pass the MQTT client to the handler
    subscription = client.create_subscription(1000, handler)  # 1000 ms (1 second) subscription interval

    # Subscribe to the temperature and humidity nodes
    temperature_handle = subscription.subscribe_data_change(temperature_node)
    humidity_handle = subscription.subscribe_data_change(humidity_node)

    print("Subscribed to temperature and humidity updates.")
    print("Listening for data changes...")

    # Keep the client running to receive updates
    try:
       while True:
            time.sleep(1)  # Keep the client alive

    except KeyboardInterrupt:
        print("Subscription interrupted by user.")

finally:
    # Clean up subscriptions and disconnect from the servers
    if 'subscription' in locals():
        subscription.unsubscribe(temperature_handle)
        subscription.unsubscribe(humidity_handle)
        subscription.delete()

    client.disconnect()
    print("Disconnected from OPC UA server.")

    mqtt_client.loop_stop()  # Stop the MQTT loop
    mqtt_client.disconnect()  # Disconnect from the MQTT broker
    print("Disconnected from MQTT broker.")
