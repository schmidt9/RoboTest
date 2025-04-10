https://github.com/airockchip/rknn_model_zoo/blob/main/examples/yolo11/python/convert.py

# run following commands from `rknn_model_zoo/examples/yolo11/python`

python convert.py /home/orangepi/sambashare/YoloTest/yolo11n.onnx rk3566 i8 /home/orangepi/sambashare/YoloTest/yolo11n.rknn

python yolo11.py --model_path /home/orangepi/sambashare/YoloTest/yolo11n.rknn --target rk3566 --img_show
