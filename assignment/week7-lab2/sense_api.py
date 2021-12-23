#!/usr/bin/python3

from flask import Flask, request, render_template
from flask_cors import CORS
from sense_hat import SenseHat

sense = SenseHat()
deviceID="device1"
#clear sensehat and intialise light_state
sense.clear()

#create Flask app instance and apply CORS
app = Flask(__name__)
CORS(app)

@app.route('/sensehat/environment',methods=['GET'])
def current_environment():
    temperature=round(sense.temperature,2)
    humidity=round(sense.humidity,2)
    msg = {"deviceID": deviceID,"temp":temperature,"humidity":humidity}
    return str(msg)+"\n"

@app.route('/sensehat/light',methods=['GET'])
def light_get():
    #check top left pixel value(==0 - off, >0 - on) 
    print(sense.get_pixel(0, 0)) 
    if sense.get_pixel(0, 0)[0] == 0:
        return '{"state":"off"}'
    else:
           return '{"state":"on"}'

@app.route('/sensehat/light',methods=['POST'])
def light_post():
    state=request.args.get('state')
    print (state)
    if (state=="on"):
        sense.clear(255,255,255)
        return '{"state":"on"}'
    else: 
        sense.clear(0,0,0)
        return '{"state":"off"}'

@app.route('/') 
def index():
    celcius = round(sense.temperature, 2)
    fahrenheit = round(1.8 * celcius + 32, 2)
    pressure = round(sense.pressure, 2)
    humidity = round(sense.humidity, 2)
    return render_template('status.html', celcius=celcius, fahrenheit=fahrenheit, pressure=pressure, humidity=humidity)

#Run API on port 5000, set debug to True
app.run(host='0.0.0.0', port=5000, debug=True)
