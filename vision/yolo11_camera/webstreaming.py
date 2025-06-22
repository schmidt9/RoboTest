# https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/

from flask import Response
from flask import Flask, request, jsonify
from flask import render_template
import threading
import argparse
import yolo11_camera

app = Flask(__name__)


@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")


@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(yolo11_camera.generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")


@app.route("/direction")
def direction():
    data = request.get_json()
    received_value = data.get('data')
    # Process the data
    response_data = {'message': f'Data received: {received_value}'}
    return jsonify(response_data)


@app.route("/message")
def message():
    data = request.get_json()
    received_value = data.get('data')
    # Process the data
    response_data = {'message': f'Data received: {received_value}'}
    return jsonify(response_data)


def run(host: str, port: int):
	# start a thread that will perform motion detection
	t = threading.Thread(target=yolo11_camera.start_capture)
	t.daemon = True
	t.start()

	# start the flask app
	app.run(host=host, port=port, debug=True,
		threaded=True, use_reloader=False)


def run_default():
    port = 8888
    print(f"Running on localhost:{port}")
    run( "0.0.0.0", port)


if __name__ == '__main__':
	run_default()
