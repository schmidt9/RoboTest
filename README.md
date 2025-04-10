https://github.com/airockchip/rknn_model_zoo/blob/main/examples/yolo11/python/convert.py

# run following commands from `rknn_model_zoo/examples/yolo11/python`

python convert.py /home/orangepi/sambashare/YoloTest/yolo11n.onnx rk3566 i8 /home/orangepi/sambashare/YoloTest/yolo11n.rknn

python yolo11.py --model_path /home/orangepi/sambashare/YoloTest/yolo11n.rknn --target rk3566 --img_show

# fix for "Invalid RKNN model version 6"
replace librknnrt.so in /usr/lib with version from this directory (taken from https://github.com/airockchip/rknn-toolkit2/blob/master/rknpu2/runtime/Linux/librknn_api/aarch64/librknnrt.so)
