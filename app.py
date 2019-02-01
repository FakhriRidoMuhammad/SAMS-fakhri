from flask import Flask
from flask import render_template, jsonify
from sensorlib.scale import Scale
from main.application import Application
from flask import request
from threading import Thread
from main.api_data import ApiData


application = Application()


def start_datalog():
    application.start()


client_id = "test_id"
country = "DE"
zip_code = 37139

data_log_thread = Thread(target=start_datalog)
# data_log_thread.start()
app = Flask(__name__)
scale = Scale()


@app.route('/')
def start():
    cal = scale.calibrated()
    return render_template('start.html', title="start", calibrated=cal)


@app.route('/calibrate')
def calibrate():
    scale.setup()
    return render_template('calibrate.html', title="calibrate")


@app.route('/tare')
def tare():
    scale.tare()
    return render_template('settings.html', title="calibrate", tare=True, client_id=client_id, country=country,
                           zip_code=zip_code)


@app.route('/reset')
def reset():
    scale.reset()
    return render_template('settings.html', title="reset", reset=True, client_id=client_id, country=country,
                           zip_code=zip_code)


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


@app.route('/debug')
def debug():
    return render_template('debug.html', title="debug")


@app.route('/settings')
def setting():
    return render_template('settings.html', title="setting", client_id=client_id, country=country, zip_code=zip_code)


@app.route('/save_id', methods=['POST'])
def save_id():
    print(request.form['hive_id'])
    return render_template('save_id.html', title="save id", hive_id=request.form['hive_id'])


@app.route('/calibrate_offset', methods=['POST'])
def config_scale():
    scale.calibrate(request.form['weight'])
    return render_template('calibrated.html', title="calibrated", weight=scale.get_data())


@app.route('/set_id', methods=['POST'])
def set_id():
    country_code = request.form['country_code']
    zip_code = request.form['zip_code']
    # hash_id = secrets.token_hex(nbytes=16)
    hive_id = "{0}-{1}-{2}".format(country_code, zip_code, hash_id)
    return render_template('confirm_id.html', title="set id", country_code=country_code, zip_code=zip_code, id=hive_id)


@app.route('/api')
def summary():
    data = ApiData()
    json_data = {}
    ds18b20data = data.get_ds18b20_data()
    dht22data = data.get_dht22_data()
    weight = scale.get_data()
    for x in range(len(ds18b20data)):
        json_data["DS1820B-{}".format(x)] = "{0} {1}".format(ds18b20data[x], "°C")

    json_data["dht22 hum"] = "{0} {1}".format(dht22data['hum'], "%")
    json_data["dht22 temp"] = "{0} {1}".format(dht22data['temp'], "°C")
    json_data["weight"] = "{0} {1}".format(weight, "KG")
    return jsonify(
        data=json_data,
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
