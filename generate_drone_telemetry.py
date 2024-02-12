# File to publish random UAV data to the MQTT BROKER

import random
import json
import uuid
import time
import paho.mqtt.client as mqtt

# CONSTANTS
MQTT_SERVER = "192.168.1.230"
MQTT_PORT = 1883

import random

class UAVTelemetry:
    def __init__(self,id, latitude, longitude, altitude, speed, heading, battery_percentage):
        self.uav_id = id
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.speed = speed
        self.heading = heading
        self.battery_percentage = battery_percentage

    def update_telemetry(self, new_latitude, new_longitude, new_altitude, new_speed, new_heading, new_battery_percentage):
        self.latitude = new_latitude
        self.longitude = new_longitude
        self.altitude = new_altitude
        self.speed = new_speed
        self.heading = new_heading
        self.battery_percentage = new_battery_percentage

    def display_telemetry(self):
        print(f"uav_id: {self.uav_id}")
        print(f"Latitude: {self.latitude}")
        print(f"Longitude: {self.longitude}")
        print(f"Altitude: {self.altitude} meters")
        print(f"Speed: {self.speed} m/s")
        print(f"Heading: {self.heading} degrees")
        print(f"Battery Percentage: {self.battery_percentage}%")
        
    def to_mqtt_message(self):
        timestamp = time.time()

        telemetry_data = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "speed": self.speed,
            "heading": self.heading,
            "battery_percentage": self.battery_percentage
        }

        mqtt_message = {
            "uav_id": str(self.uav_id),
            "timestamp": timestamp,
            "telemetry": telemetry_data
        }

        return json.dumps(mqtt_message, indent=2)

def initUAV(numberUAV):
    uav_list = []
    for _ in range(numberUAV):
        # Setting reasonable random initial telemetry values
        id = uuid.uuid4()
        latitude = 41.27555556
        longitude = 1.98694444
        altitude = round(random.uniform(0, 100),2)
        speed = round(random.uniform(0, 60),2)
        heading = round(random.uniform(0, 360), 0)
        battery_percentage = round(random.uniform(70, 100),2)

        uav = UAVTelemetry(id, latitude, longitude, altitude, speed, heading, battery_percentage)
        uav_list.append(uav)
    return uav_list


def publish_uav_telemetry(uav, client, topic):
    mqtt_message = uav.to_mqtt_message()
    client.publish(topic, mqtt_message)

def generate_correlated_telemetry(uav, duration, interval, client, topic):
    start_time = time.time()

    try:
        client.connect(MQTT_SERVER, MQTT_PORT, 60)
        
        while time.time() - start_time <= duration:
            # Simulate correlated telemetry data updates
            uav.update_telemetry(
                uav.latitude + random.uniform(-0.01, 0.01),
                uav.longitude + random.uniform(-0.01, 0.01),
                uav.altitude + random.uniform(-0.1, 0.1),
                uav.speed + random.uniform(-0.5, 0.5),
                uav.heading + random.uniform(-1.0, 1.0),
                uav.battery_percentage - random.uniform(0.01, 0.05)
            )

            # Publish telemetry data
            publish_uav_telemetry(uav, client, topic)

            print("Data sent to MQTT")
            # Sleep for the specified interval
            time.sleep(interval)
    finally:
        client.disconnect()



if __name__ == '__main__':
    number_of_uav = 1
    mqtt_topic = "testData"

    uav_instances = initUAV(number_of_uav)

    client = mqtt.Client()

    try:
        for idx, uav in enumerate(uav_instances):
            mqtt_message = uav.to_mqtt_message()
            print(mqtt_message)
            print(f"Generating Correlated Telemetry for UAV {idx + 1} for 1 minute:")
            generate_correlated_telemetry(uav, duration=600, interval=0.5, client=client, topic=mqtt_topic)
            print("Correlated Telemetry generation complete.")
            print()
    finally:
        client.disconnect()
       
    