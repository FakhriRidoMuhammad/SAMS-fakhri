from flask import Flask
from flask import render_template, jsonify
from sensorlib.scale import Scale
#from sensorlib.dht22 import DHT22
#from sensorlib.ds1820 import DS1820
from main.dataset import Dataset
from main.application import Application
from flask import request
import datetime

app = Flask(__name__)
application = Application()
scale = Scale()
dataset = Dataset()
#wire = DS1820("28-000008e2f080")


@app.route('/')
def start():
    cal = scale.calibrated()
    return render_template('start.html', title="start", calibrated=cal)


@app.route('/calibrate')
def calibrate():
    scale.setup()
    return render_template('calibrate.html', title="calibrate")

@app.route('/start_scale')
def start_calibrate():
    scale.setup()
    return render_template('start_scale.html', title="calibrate")


@app.route('/calibrate_offset')
def calibrate_offset():
    return render_template('calibrate_offset.html', title="calibrate offset")


@app.route('/measure')
def measure():
    scale.get_data()
    return render_template('measure.html', title="measure", weight=scale.measure_weight)


@app.route('/reset')
def reset():
    scale.reset()
    return render_template('reset.html', title="reset")


@app.route('/calibrate_offset', methods=['POST'])
def config_scale():
    scale.calibrate(request.form['weight'])
    return render_template('calibrated.html', title="calibrated", weight=scale.get_data())


@app.route('/api')
def summary():
    application.post_logfile()
    json_data = [{"test": "test"}]
    return jsonify(
        data=json_data,
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
