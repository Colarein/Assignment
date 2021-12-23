import socket
from time import sleep
from sense_hat import SenseHat
import logging
from dotenv import dotenv_values

#load configuration values from .env file
config = dotenv_values(".env")

logging.basicConfig(level=logging.INFO)

# Create SenseHAT object (used to access temp sensor)
sense = SenseHat()

#UDP Client configuration parameters
serverAddressPort = (config["ipAddress"],int(config["port"]))
deviceID = config["deviceID"]
interval = int(config["transmissionInterval"])

# create a socket object
socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM) 

# bind the socket object to the port
socket.connect(serverAddressPort)

logging.info(f"Connected to port: {serverAddressPort}")

while True:
    temperature=round(sense.temperature,2)
    humidity=round(sense.humidity,2)
    msgFromClient = {"deviceID": deviceID,"temp":temperature,"humidity":humidity}
    bytesToSend = str(msgFromClient).encode()
    socket.sendall(bytesToSend)
    #Log to console:
    logging.info("Sent to server: " + str(msgFromClient))
    #Sleep for 5 seconds before transmitting again. 
    sleep(interval)
