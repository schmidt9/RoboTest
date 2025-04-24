# https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/

from flask import Response
from flask import Flask
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


def run(host: str, port: int):
	# start a thread that will perform motion detection
	t = threading.Thread(target=yolo11_camera.start_capture)
	t.daemon = True
	t.start()

	# start the flask app
	app.run(host=host, port=port, debug=True,
		threaded=True, use_reloader=False)


def run_default():
	run( "0.0.0.0", 8888)


if __name__ == '__main__':
	run_default()
