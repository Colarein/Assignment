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


#Run API on port 5000, set debug to True

app.run(host='0.0.0.0', port=5000, debug=True)
