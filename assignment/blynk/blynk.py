import BlynkLib
from sense_hat import SenseHat
import time

BLYNK_AUTH = '4v7Y9VX4tse2uN2i9HvfGY82KP9m1svI'

# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

#initialise SenseHAT
sense = SenseHat()
sense.clear()

# register handler for virtual pin V1 write event
@blynk.on("V0")
def v3_write_handler(value):
    buttonValue=value[0]
    print(f'Current button value: {buttonValue}')
    if buttonValue=="1":
        sense.clear(255,255,255)
    else:
        sense.clear()

#tmr_start_time = time.time()
# infinite loop that waits for event
while True:
    blynk.run()
    blynk.virtual_write(1, round(sense.temperature,2)) #Links temp to mobile
    blynk.virtual_write(2, round(sense.pressure,2)) #links pressure to mobile
    blynk.virtual_write(3, round(sense.humidity, 2)) #links humdity to mobile
    time.sleep(1)

