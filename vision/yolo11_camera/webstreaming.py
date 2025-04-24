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


def run(args):
	# start a thread that will perform motion detection
	t = threading.Thread(target=yolo11_camera.start_capture)
	t.daemon = True
	t.start()

	# start the flask app
	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)


def run_local():
	run(["--ip", "0.0.0.0", "--port", 8888])


if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	args = vars(ap.parse_args())

	run(args)
