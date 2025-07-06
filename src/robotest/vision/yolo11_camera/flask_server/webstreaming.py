# https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/

from flask import Response
from flask import Flask, request, jsonify
from flask import render_template
import threading
import robotest.speech.speak as speak
import robotest.keyestudio.i2c_master as i2c_master
import robotest.keyestudio.commands_helper as commands_helper
from robotest.utils.settings import settings
from robotest.vision.yolo11_camera import yolo11_camera

app = Flask(__name__)


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(
        yolo11_camera.generate(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/direction", methods=["GET", "POST"])
def direction():
    data = request.get_json()
    received_value = data.get("data")

    commands_helper.send_direction_command(received_value)

    # Process the data
    response_data = {"message": f"Data received: {received_value}"}
    return jsonify(response_data)


@app.route("/flashlight", methods=["GET", "POST"])
def flashlight():
    data = request.get_json()
    received_value = data.get("data")

    commands_helper.send_flashlight_command()

    # Process the data
    response_data = {"message": f"Data received: {received_value}"}
    return jsonify(response_data)


@app.route("/message", methods=["GET", "POST"])
def message():
    data = request.get_json()
    received_value = data.get("data")

    speak.speak(received_value)

    # Process the data
    response_data = {"message": f"Data received: {received_value}"}
    return jsonify(response_data)


@app.route("/speed", methods=["GET", "POST"])
def speed():
    data = request.get_json()
    received_value = data.get("data")

    commands_helper.save_and_send_speed_command(received_value)

    response_data = {"message": f"Data received: {received_value}"}
    return jsonify(response_data)


@app.route("/get_speed", methods=["GET"])
def get_speed():
    return settings.toJSON()


def run(host: str, port: int):
    # start a thread that will perform motion detection
    t = threading.Thread(target=yolo11_camera.start_capture)
    t.daemon = True
    t.start()

    commands_helper.send_settings_to_i2c_slave()

    speak.start_server()

    app.run(host=host, port=port, debug=True, threaded=True, use_reloader=False)


def run_default():
    port = 8888
    print(f"Running on localhost:{port}")
    run("0.0.0.0", port)


if __name__ == "__main__":
    run_default()
