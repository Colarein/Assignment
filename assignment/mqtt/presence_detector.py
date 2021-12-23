#!/usr/bin/env python3
#coding=utf-8

import subprocess

#dictionary of known devices 
devices = [{"name":"Sense Pi", "mac":"DC:41:A9:D5:86:DF"},
        {"name":"Google Home", "mac":"D4:F5:47:6B:95:AC"}
        ]
import logging

logging.basicConfig(filename='presence_detector.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Returns the list of known devices found on the network
def find_devices():
    output = subprocess.check_output("sudo nmap -sn 192.168.0.30/24 | grep MAC", shell=True)
    devices_found=[]
    for dev in devices:   
        if dev["mac"].lower() in str(output).lower():
            logging.info(dev["name"] + " device is present")
            devices_found.append(dev)
        else:
            logging.info(dev["name"] + " device is NOT present")
    return(devices_found)

# Main program (prints the return of arp_scan )
def main():
    print(find_devices())

if __name__ == "__main__":
    main()
