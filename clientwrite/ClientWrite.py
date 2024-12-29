import time
import random
from opcua import Client, ua

# OPC UA server details
url = "opc.tcp://host.docker.internal:62640/IntegrationObjects/ServerSimulator"  
temperature_node_id = "ns=2;s=Tag7"  
humidity_node_id = "ns=2;s=Tag6"        

# Function to generate random values 
def generate_random_temperature():
    return round(random.randint(20, 70), 1) 

def generate_random_humidity():
    return random.randint(30, 80)  

# Create a client instance
client = Client(url)
def main():

    # Connect to the OPC UA server
    client.connect()
    print("Connected to OPC UA server.")

    # Get the nodes for temperature and humidity
    temperature_node = client.get_node(temperature_node_id)
    humidity_node = client.get_node(humidity_node_id)

    print("Sending data...")
    while True:
        temperature_value = generate_random_temperature()
        humidity_value = generate_random_humidity()

        # Write temperature
        temperature_node.set_value(ua.Variant(temperature_value, ua.VariantType.Float))
        print(f"Temperature set to {temperature_value} °C")

        # Write humidity
        humidity_node.set_value(ua.Variant(humidity_value, ua.VariantType.Int32))
        print(f"Humidity set to {humidity_value} %")

        # Wait for 2 seconds before sending the next set of values
        time.sleep(2)
if __name__ == "__main__":
    main()