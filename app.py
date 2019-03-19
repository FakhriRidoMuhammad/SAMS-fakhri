from flask import Flask, render_template, jsonify, request
from sensorlib.scale import Scale
from main.application import Application
from threading import Thread
from main.api_data import ApiData

application = Application()


def start_main_app():
    application.start()


scale = Scale()  # Scale for /api data
data_log_thread = Thread(target=start_main_app)  # Thread to start main application

if scale.calibrated():  # is scale calibrated, start the main application
    data_log_thread.start()

app = Flask(__name__)


@app.route('/')
def start():
    cal = scale.calibrated()
    return render_template('start.html', title="start", calibrated=cal)


@app.route('/calibrate')  # start calibrate the scale
def calibrate():
    scale.setup()
    return render_template('calibrate.html', title="calibrate")


@app.route('/calibrate_offset')  # calibrate the offset starting
def calibrate_offset():
    return render_template('calibrate_offset.html', title="calibrate offset")


@app.route('/quick_start')  # start quick calibrate the scale
def quick_start():
    return render_template('quick_start.html', title="quick start")


@app.route('/quick_setup')
def quick_setup():
    scale.calibrate(10000)  # quick calibrate the scale with 10 Kg
    cal = scale.calibrated()
    return render_template('calibrated.html', title="calibrate offset", calibrated=cal)


@app.route('/calibrate_offset', methods=['POST'])  # send known weight to calibrate
def config_scale():
    scale.calibrate(request.form['weight'])
    cal = scale.calibrated()
    return render_template('calibrated.html', title="calibrated", calibrated=cal)


@app.route('/settings')  # setting page
def settings():
    return render_template('settings.html', title="setting")


@app.route('/settings', methods=['POST'])
def setting():
    # is tare or reset posted to settings?
    try:
        if request.form.get("reset") == "":
            scale.reset()
        if request.form.get("tare") == "":
            scale.tare()

    except Exception as e:
        print(e)

    return render_template('settings.html', title="setting")


@app.route('/api')  # need api data to debug sensors
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
