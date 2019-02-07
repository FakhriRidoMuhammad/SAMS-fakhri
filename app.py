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
data_log_thread.start()
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


@app.route('/start_scale')
def start_calibrate():
    scale.setup()
    return render_template('start_scale.html', title="calibrate")


@app.route('/calibrate_offset')
def calibrate_offset():
    return render_template('calibrate_offset.html', title="calibrate offset")


@app.route('/calibrate_offset', methods=['POST'])
def config_scale():
    scale.calibrate(request.form['weight'])
    return render_template('calibrated.html', title="calibrated", weight=scale.get_data())


@app.route('/settings')
def settings():
    return render_template('settings.html', title="setting")


@app.route('/settings', methods=['POST'])
def setting():
    try:
        if request.form.get("reset") == "":
            scale.reset()
        if request.form.get("tare") == "":
            scale.tare()

    except Exception as e:
        print(e)

    return render_template('settings.html', title="setting")


@app.route('/api')
def summary():
    api_data = ApiData()
    json_data = api_data.get_data()

    try:
        weight = scale.get_data()
        json_data["weight"] = "{0} {1}".format(weight, "KG")
    except Exception:
        json_data["weight"] = "scale not properly connected"

    return jsonify(
        data=json_data,
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
