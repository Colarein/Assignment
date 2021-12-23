import socket
from time import sleep
from sense_hat import SenseHat
import logging
from dotenv import dotenv_values

#load configuration values from .env file
config = dotenv_values(".env")

logging.basicConfig(level=logging.INFO)

# Create SenseHAT object (used to access temp sensor when creating message)
sense = SenseHat()

#UDP Client configuration parameters
serverAddressPort = (config["ipAddress"],int(config["port"]))
deviceID = config["deviceID"]
interval = int(config["transmissionInterval"])

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

logging.info(f"Listening for UDP Datagrams on port: {serverAddressPort}")

while True:
    temperature=round(sense.temperature,2)
    pressure=round(sense.pressure,2) 
    humidity=round(sense.humidity,2)
    msgFromClient = {"deviceID": deviceID,"temp":temperature,"pressure":pressure,"humidity":humidity}
    bytesToSend = str(msgFromClient).encode()
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)      
    #Log to console:
    logging.info("Sent to server: " + str(msgFromClient))
    #Sleep for 5 seconds before transmitting again. 
    sleep(interval)
